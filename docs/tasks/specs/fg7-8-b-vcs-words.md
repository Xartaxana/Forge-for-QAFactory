# FG7-8 part B — the words of gate A's test-repository question get rows, an executor and a record (B-13)

Draft by the designer, task t-106; REVISED as t-115 after the critic on the plan (t-109, `fit_with_fixes`) and the
wave-0 measurement B0 (t-110). Node `forge/7/FG7-8` item 4, feature F19, 12.11.2026. Forks are returned (§5), not
decided, except where the Lead decided them (marked "Lead, t-115"). Part A of the node (t-105: `question_register.matches`
/ `row_answered`) lands first and does not touch `check_vcs`; §4.0 says what lands after what.

Owner's words folded in:
- 12.11.2026 (relayed during t-106): **the factory MAY itself run `commit` and `stash` in the person's test repository
  when the person answers with that word.**
- 12.11.2026 (relayed during t-115), verbatim: «нет, в отчёте это не надо, но нужно напомнить в чате. И фабрика должна
  различать это она сама накидала своих файлов или это действительно были изменения человека». Read as two duties:
  (OW-1) no report section and no new record file for a stash (F3 stays (a)), but the person is REMINDED IN THE CHAT
  that their changes sit in a stash (or were committed) and how to take them back — right after the action and once more
  in the run's closing message (§3.8); (OW-2) the dirty set shown, and the set commit/stash take, are the PERSON's
  changes only; files the factory itself wrote in the test repository are never shown as "your uncommitted changes" and
  never committed or stashed under the person's word (§3.7, fork F12 on the carrier). OW-2 lifts the old non-goal "how
  gate A detects the VCS state" for exactly this.

### Lead acceptance of the draft (12.11.2026, t-106)

The draft is accepted as the plan that goes to the critic on the plan. Forks of §5, decided by the Lead on the
designer's recommendations ("by recommendation, until the owner's word" where marked):

- **F1 = (a)**, by recommendation, until the owner's word: exactly the set the person was shown, outside
  `qa-factory/`, one commit, a factory-written message naming the story, the repository's own identity, the person's
  hooks running. The `says` line names "product code included" when the tests live in the product's repository.
- **F2 = (a)**: follows P8 directly — a run that leaves no trace neither offers nor runs `commit` / `stash`.
- **F3 = (a)**: the waiver's decision text carries the facts and the undo; no new record file. Whether a stash is
  listed under "Left with you" in the report is asked of the owner; (b) opens as its own node if she says yes.
  (Owner, 12.11.2026: not in the report; a reminder in the chat instead — OW-1.)
- **F4 = (a)**, **F5 = (a)**, **F6 = (a)** (B5 is filed as a finding into an untaken batch), **F7 = (a)**.

B0 (the measurement) runs now, beside the critic on the plan; its table becomes F0-23. B1 waits for part A on `main`.

### Lead decisions on the critic's verdict (t-115), written in as decided

1. B-1/B-2/B-3: the change set is read with `git status --porcelain=v1 -z`; refusals come BEFORE any write; success is
   judged on the repository state afterwards, never on the exit code alone; a failure is restored from a tree written
   before the add (`write-tree` / `read-tree`), never `git reset -- <paths>`; the undo text is the one TRUE for the
   case. Every command form here is one B0 or the critic ran, or a B0-2 row (§3.5).
2. B-4: the executor refuses any path under the factory folder (both rename sides) by the gate's own reader; the guard
   rules are asked only in the form they accept (§3.6).
3. B-5: commit/stash are offered only when the person was shown EVERY path they take; a cap (proposed 20, fork F10);
   above it only `go on` and `accept`.
4. B-6: B1 owns `_finding_forms`.
5. B-7: the record fits `waiver.py` as it is today (no change to `waiver.py`), §3.4.
6. B-8: the gate stores what it showed on both roads; the CLI compares against the STORED block; one writer, one
   reader (§3.3).
7. B-9: a repository write is never run on a word the conductor inferred; other words → the conductor asks once for the
   exact word, and only that exact answer runs the command.
8. B-10: B2 owns the census row; the ratchet change is named row by row.
9. F-1..F-16 folded in or answered (§9); F-14 stays an owner question (§5, Q-1).

### Lead acceptance of the revision (12.11.2026, t-115)

The revision is accepted. Forks of §5, decided by the Lead on the designer's recommendations:

- **F9 = (a)**, **F10 = 20 paths**, **F11 = (a)**, **F13 = (a)**, **F14 = (a)** (B2 reports whether the note is
  delivered on a clean pass; (b) opens as a node if not), **F15 = (a)**, **F16 = (a)**.
- **F12 = (a)**: the owner's word OW-2 needs a carrier, and (b) would hide a hand-edited factory test, against that
  word. Node B6 is new architecture (a new record, a hook on every role write), so §3.7 and B6 — and only they — get
  one more critic pass on the plan before B6 and B1's `factory_origin` are built (PROJECT.md, new idea, step 6).
- **Q-1** goes to the owner; until her word (a): allowed, `says` names "product code included".

Order from here: B0-2 (measurement) and the critic on §3.7/B6 run now, side by side; B1 and B6 start when both are
accepted; then B2 and B3; one code critic for the topic.

### Lead decision on the critic's verdict on §3.7/B6 (12.11.2026, t-119, `reviews/t-119-fg7-8-b6-plan.md`)

The verdict (`fit_with_fixes`, 4 blocking) stands and changes the order, not the words' executor:

1. **OW-2 leaves this spec's build path and becomes its own node, waiting for the owner.** B-4: `check_vcs` runs
   only at gate A, before S5 writes a test, so on a first pass the story's own record is empty; the factory's files a
   person sees then are an EARLIER story's (or an earlier pass's), which §3.7 calls the person's. Which files the
   owner meant is her reading (rule 11a). B-1/B-2/B-3 (a person's edit absorbed by a later factory Edit; the
   orchestrator's writes on the skill road; no role attribution on the skill road) need a pre-image chain and a
   per-road attribution — a mechanism of its own, with its own critic on the plan.
2. **B6 is NOT built now. `factory_origin` is NOT built in B1.** B1 builds `vcs_changes` with `person` = every entry
   outside the factory home and `factory` = `[]` (the "no record" world of F12's note: today's behaviour, never the
   unsafe side). The digest, the list, the cap and the blockers are computed over `person` exactly as written, so the
   later node adds one reader and no caller changes. Every sentence of §3.7 rules 1–3, of B1's `factory_origin` rows
   and of F13 is DEFERRED to that node; B1's builder skips them.
3. Fact correction F-1 is taken: manifest rows carry the whole test-file sha256 (`trace_binding.test_content_sha`),
   so F0-30's "no content record anywhere" is false for test bodies; F12 is re-decided inside the deferred node.
4. Owner questions carried by the Lead: (Q-1) product code under `commit`/`stash`; (Q-2) "files the factory left in
   your repository from an earlier story or an earlier pass — the factory's (not shown, not taken) or yours?".
   OW-1 (the reminder in the chat) is unaffected and is built now.
5. **Owner's word on Q-2 (12.11.2026): «Фабричными»** — files the factory left in the person's repository from an
   earlier story or an earlier pass are the FACTORY's: not shown as the person's uncommitted changes, not taken by
   `commit`/`stash`. So the deferred node is built on the critic's "if she says the factory's" branch: the record is
   project-level (`qa-factory/state/factory-writes.jsonl`, `story` in every row), each row carries the file's state
   before the write, and a path is the factory's only on an unbroken chain of rows back to a committed state (a hand
   edit breaks the chain → the person's). It gets its own designer draft and critic on the plan (B-1, B-2, B-3 of
   t-119 are its entry requirements) and does not hold B1–B3 or the release.

---

## §0 Facts (read in the carrier, file:line; re-read 12.11.2026 for t-115 where marked *)

| # | Fact | Carrier |
|---|---|---|
| F0-1* | `Rehearsal.check_vcs` (`:1917-1953`) writes two `person_decides` findings with `subject="test-repo"` (id `vcs-test-repo`). Dirty branch `fix`: literal `"answer with your approval: commit, stash, or go on on this branch"` (`:1946`) + `waiver_command(block)`. Clean branch `fix`: `"answer with your approval: this branch, or name another"` (`:1952`). | `scripts/gate_preflight.py` |
| F0-2* | The door block is `test repository state: <HEAD[:12]>` (`:1939`). No HEAD, no door. | `gate_preflight.py:1936-1939` |
| F0-3* | Dirty = `outside_factory_home(status --porcelain lines, _factory_home_in_repo(root, tests_root))` (`:1932-1935`). `_factory_home_in_repo` (`:223-234`) returns the home relative to the top with `/`, or `""` when it cannot be told (no git answer, or the home lies outside that tree). `outside_factory_home` (`:244-258`) drops a line only when EVERY path is under the home; a rename with one side outside stays. Message names the first 5 paths and "and N more" (`:1944-1945`). `_factory_home_in_repo` has one package caller (`check_vcs`); `outside_factory_home` is also read by `tests/test_ahead_cards_rules.py` (quarantined). | `gate_preflight.py` |
| F0-4* | `_git` read-only, 10 s timeout, no prompts, None on non-zero exit (`:210-220`). | `gate_preflight.py` |
| F0-5 | `door(block, stage, option, row)` appends `{block (cut at 60), stage, option}` to `waives` (`:1318-1326`); `waiver_command` (`:1338-1353`); `add` drops a finding a recorded word passes (`:1394-1414`). | `gate_preflight.py` |
| F0-6* | `render` prints `  - [id] message` then `      fix: <fix>` (`:5811-5814`). `brief_lines` (`:5917-5991`) prints `- [your call] <message>` cut at `BRIEF_CUT = 200` (`:1014`), the `fix` only for `story_level` rows, at most `limit=5` rows, then "+N more — the whole list is under "Rehearsal of gate A" below". | `gate_preflight.py` |
| F0-7 | `FINDING_DOOR_OPTIONS = ("product_gap",)` (`:776`); `finding_door_words` (`:779-793`); `finding_door_option` (`:796-809`); `finding_door_word_of` (`:812-814`); `_word_key` (`:709-714`). | `scripts/gate_brief.py` |
| F0-8* | `_finding_forms` (`:2854-2876`) offers only `<item id>: accept <your reason>` and `approve as is`; `answer_forms` (`:2894-2904`) is "EVERY form of an answer this gate-A packet offers"; `ANYTHING_ELSE_SENTENCE` (`:1046`). | `gate_brief.py` |
| F0-9 | `finding_door_words` vocabulary block has one row, `product_gap`. | `references/question-vocabulary.json:91-101` |
| F0-10* | `Driver.read_finding_doors` (`:3078-3185`): `_FINDING_LINE_RE` (`:3076`); a line is read only if the id is a finding of this rehearsal, the packet carried `[id] message`, the stored `shown_doors[id]` equals the current `waives` (`:3150-3153`), no `?`, a known word; last line per id wins. | `scripts/driver_machine.py` |
| F0-11* | `_stand_gap_lines` (`:2769-2801`) reads `self.state["shown_doors"][gate]` at `:2793`. `_record_door_lines` (`:2837-2877`): a `product_gap` branch keyed on `door["option"]` (`:2847`) and a generic waiver branch `waiver.py --stage <door stage> --block <block> --decision said *waiver_road()` (`:2864-2866`). | `driver_machine.py` |
| F0-12* | `_relay_note` (`:2908-2969`) builds the conductor's note: recorded lines (`:2916-2918`), probed containers, unread lines with `door_keys` (`:2937-2940`). | `driver_machine.py` |
| F0-14* | `rule_pathspec(command: str) -> str` (`stage_guard.py:2361-2396`): "" or a refusal; checks only `-a/--all` and that paths or `--` are present; never the factory folder. `rule_stash(command: str) -> str` (`:2410-2442`): refuses a saving stash without `--`, or one whose paths after `--` name the factory (`_names_factory`: `FACTORY_PATH_RE` or any path ending in `qa-factory`, `:2399-2401`). Both cut the tail at ` && `, ` || `, `;`, `\n`, ` | ` before `shlex` (`:2325-2328`, `:2350-2353`). `rule_manifest(ticket, what, event, *, required, pipeline, task_root)` (`:1037`) is not a command-text function. | `scripts/stage_guard.py` |
| F0-15* | `external_writes.closed_by_run(task_root) -> str` (`:189-202`): truthy only when `pipeline.no_trace`; an unreadable pipeline closes NOTHING. | `scripts/external_writes.py` |
| F0-16 | conductor-actions row precedent `product_gaps.py record ... --words-file` (`:30`). | `references/conductor-actions.json` |
| F0-17 | `s4.md:159-163` skill road records `<check id>: accept`; `conductor.md:21`. | phases / references |
| F0-18 | `halts.md:19` and two eval files still offer the old four S5 words. | read |
| F0-19* | Test layers (`test-layers.json`): `keep` is `:35-6896`, `quarantine` starts `:6951`. Keep: `test_gate_preflight.py` (`:1844`, gate_named), `test_gate_question_form.py` (`:1900`, AR-16 detector), `test_gate_vocabulary.py` (`:2009`), `test_guard_window_files.py` (`:2145`), `test_hooks_wiring.py` (`:2383`), `test_judgment_census.py` (`:2690`), `test_state_exits.py` (`:5291`), `test_words_doors.py` (`:6832`, sole AR-24 detector), `test_artifact_writers.py` (`:120`). Quarantine (never edited): `test_ahead_cards_rules.py` (`:7001`), `test_decision_classes.py` (`:7694`), `test_test_repo_base.py` (`:10178`), `test_d1_product_gap.py`. | `scripts/tests/test-layers.json` |
| F0-20* | Census: `check_vcs` row `safety`/`intent` (`:340`); ratchet `safety: 54`, `word-list: 0`, `breach: 1` (`:4`); the ratchet is DENSE (a count below its ceiling is red too, `test_judgment_census.py:368-376`). `UNIT_NAME_RE` (`test_judgment_census.py:61`) makes any function named `run`/`_run`, `check_*`, `rule_*`, `judge*`, `validate*`, `refuse*`, `*_check`, `*_errors`, `*_problems` a unit; u3: a body that raises `ValueError`/`StateConflict` or calls `deny`/`block`. | `fixtures/judgment-census.json`; the test |
| F0-21 | SIBLING_MAP axis 5 row 139, row 137; axis 34 (`:580-590`). | `docs/SIBLING_MAP.md` |
| F0-23* | **B0 (t-110), git 2.56.0.windows.2**: `git add -- p` + `git commit -m m -- p` and `git stash push --include-untracked -m m -- p` take exactly the listed entry and leave a dirty `qa-factory/` untouched for classes `??` file, `??` folder, ` M`, `M `, `MM`, ` D`, `A `, and space/non-ASCII ONLY with the unquoted path (submodule: commit only). `git add` exits 128 on `D ` and `R ` (both sides), so a mixed tree fails whole; stash on `D `/`R ` exits 128 AND leaves a stash entry with the tree unchanged; a quoted path: commit 128, stash exit 0 "No local changes to save"; submodule stash: exit 0, no-op. Commit of `MM` takes the WORKTREE content. `reset --soft HEAD~1` restores the before-porcelain only for `M ` and `A `. Plain `stash pop` loses staging; `pop --index` restores `M ` and `MM`. | `docs/tasks/specs/reports/t-110-b0-git-measure.md` |
| F0-24* | **Critic probes (t-109)**: `g3` `UU` in a merge: `git add -- c.txt` exit 0 stages the markers; `git commit -- ...` exit 128 "cannot do a partial commit during a merge"; `git reset -q -- paths` destroys the conflict stages. `g4`: `git add -- <entries with a worktree change>` then `git commit -m QA -- <all paths, both rename sides, staged deletes>` exit 0 on `D `+` M`+`R `+`??`; `git show --name-status HEAD` = `D/M/R100/A`; tree clean; the critic read the change set there with `--porcelain=v1 -z`. `g4-s`: stash of staged D+R with `:(top,literal)` pathspecs exit 128 and an entry left. `g1`: `reset --soft` after commit loses the `MM` split. | `docs/tasks/specs/reviews/t-109-fg7-8-b-plan.md` |
| F0-25* | **The skill road's packet is `gate_brief` only.** `gate_brief.main` (`:5061-5110`), off the driver (`RUN_MODE_ENV != driver`), prints the brief, calls `keep_shown_attachments(task_root)` (writes `state/driver-state.json` `shown_attachments`, `:3328-3356`, guarded: folder exists, no current approved gate A decision, file a JSON object) and `write_gate_message` (`work/gate-a-message.md`). `s4.md:202`: the message is that file "printed whole". It has NO "Rehearsal of gate A" section: the driver appends that section itself (`driver_gates.gate_text`, `:120-124`, `gate_preflight.py --text`). So on the skill road a finding's `fix` and any path beyond `brief_lines`' five rows are never shown. | `gate_brief.py`; `driver_gates.py`; `s4.md` |
| F0-26* | The driver stores what it showed: `Driver.gate` (`driver_gates.py:312-313`) sets `self.state["shown_doors"][gate]` from `last_rehearsal_doors`; the driver's state file is `state/driver-state.json` (`driver_core.py:530`, `:585`) — the SAME file `gate_brief.ATTACHMENTS_STATE_FILE = "driver-state.json"` (`gate_brief.py:3243`) names. | `driver_gates.py`; `driver_core.py`; `gate_brief.py` |
| F0-27* | `gate_brief.render` (`:3830-3882`): the cover-sheet cap `MAX_LINES = 40` (`:63`) truncates the brief, grown only by named bounded blocks (`:3868-3877`). | `gate_brief.py` |
| F0-28* | `waiver.py main` (`:1566-1654`): the `--stage/--block` form takes the words from `--decision` OR `--words-file`, never both (`person_words.read`, `person_words.py:136-156`, refuses both); `--remark --stage --text|--words-file` keeps words with no pass (`:1638-1641`); `--by` is free text (default `human`; `person_owned.DRIVER_BY = "driver"`). `person_words.write_words(task_root, dispatch_id, kind, text)` (`:172`) is the one writer of `state/words/`. | `scripts/waiver.py`; `person_words.py`; `person_owned.py:138` |
| F0-29* | `state/test-repo-base.json` (writer `stage_done.py S0` via `test_repo_base.s0_line`; reader `test_repo_base.load(task_root) -> dict | None`, never raises): at S0, every uncommitted path of the WHOLE repository with `status` and working-tree `sha256` (`""` for a non-file), up to `DIRTY_LIMIT = 2000` with `dirty_truncated`; the factory folder excluded; written ONCE (a resume keeps it); `late: true` when written after the story already produced evidence. | `scripts/test_repo_base.py:1-88` |
| F0-30* | What the factory wrote in the test repository is NOT recorded with content anywhere: `automation-manifest.json` `tests[].file` (reader `proof_level.test_file_of`, `contract.manifest_tests`) names the test files, without a whole-file hash (a case-insensitive Grep of `manifest_put.py` for `sha256|home_hash` finds only the marked-line `home_hash`); helpers are not listed; `state/window-files/` claims (`window_files.py`) hold test files only and are released at a window's close. No package hook records a role's Write/Edit outside `qa-factory/` (PostToolUse `Write|Edit` runs only `validate_artifacts.py`, a validator that writes nothing, `hooks.json:66-75`; FR-45). | the files named; Grep trail §8 |
| F0-31* | The story-end seam on both roads: driver `story_step.give_back_config` at every terminal exit (`driver_machine.py:1375-1378`, `:1938-1940`; the done Stop text `"<task>: the story is finished; nothing is pending."`); skill `story_step.py config-restore` prints one JSON line whose `line` the conductor tells "as it stands" (`s9.md:25`). | `story_step.py:845-885`; `driver_machine.py`; `s9.md` |

---

## §1 Scope, invariants, AR-n

**Goal.** Each word that gate A's test-repository question offers is a data row with a named executor. The question is
about the PERSON's uncommitted changes, listed whole. A word the person writes reaches ONE executor on both roads; the
action is done, checked on the repository's state and recorded, or fails with a door; the person is told in the chat
what was done and how to take it back, then and at the end of the run.

**In scope:** the dirty-tree finding of `check_vcs`, its three words `commit`, `stash`, `go on`; the change-set read it
rests on (now `-z`, and split into the person's and the factory's entries, OW-2); the reminder (OW-1).
**Non-goals** (the Lead's): code; part A; the clean-tree literal and `check_stand` (queued B5); new words beyond the
three; a report section for a stash (owner: no).

### Invariants (each named edge protects one of these)

- **I-1 Nothing is promised that nothing executes.** A word the packet offers has a row, a reader and one executor on
  both roads, and its executor would not refuse the repository as it stands at show time (FR-9, axis 5 row 139).
- **I-2 A repository write takes exactly what the person was shown.** Every path a commit or stash takes was listed
  whole in the packet the person read, on that road; the set equals the shown one (same HEAD, same digest of the
  person's entries); never the factory's folder; never a factory-written file; never a path the guard cannot read
  whole. Any difference: nothing runs.
- **I-3 A repository write is never inferred.** `commit`/`stash` run only on the closed word read whole, no `?`, on a
  door the shown packet carried — read by code on the driver road, and on the skill road (and after a relay) only after
  the person answered with the exact word; no role maps other words onto a write (FR-12, P27).
- **I-4 A ban is never bypassed.** The person's hooks run; no `--no-verify`, no `-c`; the guard rules are asked as a
  second layer and a refusal of theirs stops the write (FR-57).
- **I-5 An answered boundary is not re-asked** (FR-7) — unless re-asking is the only way to keep I-2 (a hook left the
  tree dirty): then I-2 wins and the question comes again.
- **I-6 A failure is the factory's to report.** No pass is recorded on a failure or a no-op; it reaches the conductor
  once with git's text and the true state (FR-3, P22).
- **I-7 A no-trace run writes nothing into the project's repository**, and a pipeline that cannot be read counts as
  no-trace for this write (P8, FR-53, AR-28).
- **I-8 The person's own work is never lost without a true undo.** Staged splits (`MM`), conflict stages and stash
  entries are restored or named exactly; an undo text is the one measured true for the case (AR-25).
- **I-9 The person's change is never hidden** (OW-2, FR-59). An entry is the factory's only when a record proves the
  current bytes are the factory's own writing; anything else — no record, an unreadable record, a hand edit, a path
  dirty at S0 — is the person's.

### Architecture invariants touched and the change check each demands (copied into the node DoDs)

| AR | How it is kept | Change check |
|---|---|---|
| AR-1 | Words are rows with `executor`/`writes_repository`; code reads the capability key, never the word. | Grep `"commit"|"stash"|"go on"` in the touched functions of `gate_preflight.py`, `gate_brief.py`, `repo_words.py`: no hit outside docstrings. |
| AR-9 | Every refusal/problem names what it expected and a door (person: "commit or stash it yourself, then answer `vcs-test-repo: go on`"; conductor: the command). | B2 test rows read the door sentence per problem. |
| AR-13 | One read of the change set (`gate_preflight.vcs_changes`, `-z`); one state block (`vcs_state_block`); one blocker list (`vcs_blockers`); one factory-home reader (`factory_home_place`, `_factory_home_in_repo` delegating); one origin reader (`factory_origin`); one store/reader of shown doors (`gate_brief.keep_shown_doors` / `shown_doors_of`); one commit/stash message builder (`repo_words.message`). | Grep `status", "--porcelain` and `test repository state:` in `scripts/`: only in the helpers. |
| AR-14 | Waivers: `waiver.py`; `shown_doors`: `gate_brief.keep_shown_doors` (driver and skill); `state/factory-writes.jsonl`: `factory_writes.record` (B6) with an `artifact-writers.json` row. | `test_artifact_writers.py` in B6's witness. |
| AR-15 | The survivor of "never the factory's folder" is `factory_home_place` read per path; the guard (`rule_pathspec`/`rule_stash`) is the survivor of the command FORM, asked second. | B2 rows: a rename from `qa-factory/x` refused by the executor; the built argv passes both rules. |
| AR-16 | Hint lines from rows with rule-6 price lines, through `human_text.problems`; the forms list carries every offered word (B-6). | `test_gate_question_form.py` rows. |
| AR-17 | Problems reach the conductor through the existing relay; no new stop. | No new `Person`/`Stop` class. |
| AR-19 | Driver road and skill road call ONE executor (`repo_words.run`) and ONE shown-doors reader. | Axis 5 row (B4). |
| AR-20 | Census `safety` 54 → 55 for `repo_words.run` only; every other ceiling unchanged. | Named in B2's verdict. |
| AR-22 | New fields (`answers`, `executor`, `writes_repository`, `shown_doors` on the skill road, `factory-writes.jsonl`) each name producer and reader (§3). | Rows. |
| AR-24 | The person's line reaches the record whole (`person_decision`), the CLI takes `--words-file`. | `test_words_doors.py` row. |
| AR-25 | New states "committed / stashed on the person's word" name their true undo (B0-2 measured) in the record and `state-exits.md`. | `test_state_exits.py`. |
| AR-28 | Unreadable vocabulary, HEAD, change set, pipeline, shown record or origin record never becomes a pass or a hidden entry. | Rows in B1/B2. |
| AR-29 | Checks are data/safety; the reading of other words stays the person's (they re-answer), never a role's mapping. | `test_judgment_census.py`. |

### §1.1 Every check this spec adds or alters: owner and census class

| Check | Where | Owner | Census class |
|---|---|---|---|
| A vocabulary row is dropped unless option/executor/word are valid | `gate_brief.finding_door_words` | data | shape (not a unit by name) |
| A repository-writing word is read only alone (F5) | `gate_brief.finding_door_option` | intent | word-list over the CLOSED vocabulary; not a unit by name |
| Repository-writing doors are not registered in a no-trace/unreadable run, above the cap, or when `vcs_blockers` names the word | `gate_preflight.check_vcs` | intent | safety (existing row, unchanged class) |
| An entry is the factory's only on a matching record | `gate_preflight.factory_origin` | data | not a unit by name (a helper of two rows: `check_vcs`, `repo_words.run`) |
| Shown block = stored block = fresh digest; class blockers; per-path home; guard; post-state | `repo_words.run` | intent | **safety, new row** |
| The CLI's words file reads as the exact word (fork F9) | `repo_words.main` → `finding_door_option` | intent | not a unit (no refusal site: returns an exit code) |

---

## §2 Behaviour in one paragraph

Gate A's rehearsal reads the change set once with `-z -uall` (G1) and splits it: entries a record proves the factory
wrote are the factory's (one note line, never asked about, never taken); every other entry is the person's. When the
person has entries, `vcs-test-repo` lists them ALL (up to the cap), with one line per offered word and its three price
lines, in a block both roads print. Doors: `accept`, `go on`, and — unless the run leaves no trace, the list is over the
cap, or a blocker forbids the word — `commit` and `stash` on the block `test repository changes: <head12> <digest12>`.
The packet's doors are stored when it is shown, on both roads, by one writer. The person writes `vcs-test-repo: commit`.
Driver road: `read_finding_doors` reads it against the stored doors, `_record_door_lines` calls `repo_words.run` with
the shown block. Skill road (and after a relay): the conductor runs `repo_words.py --word commit --words-file <the
person's exact answer>`, which takes the block from the stored record. `run` re-reads the change set, refuses on any
difference or blocker, writes a tree of the index, runs git, judges the result on the state, and returns facts; the
caller records the person's word with them; the person is told what was done and how to undo it, and is reminded at
the end of the run if the stash or the commit still stands.

---

## §3 Shared definitions

### §3.1 Data: three rows in `question-vocabulary.json` `finding_door_words.answers`

As t-106 (`option`/`word`/`executor`/`writes_repository`/`says`/`factory`/`you`/`story`/`synonyms`), with these text
changes: `vcs_commit.says` = "I commit all your uncommitted changes listed above, each file as it is on disk now, on
this branch, with a message that names this story"; `vcs_stash.says` = "I put all your uncommitted changes listed
above aside in a git stash named after this story"; `vcs_stash.you` = "work of yours outside the factory: taking them
back from the stash when you want them (I remind you how)". `product_gap` gains `"executor": "product_gap"`.
`FINDING_DOOR_OPTIONS` += `vcs_commit`, `vcs_stash`, `vcs_go_on`; `FINDING_DOOR_EXECUTORS = ("product_gap", "record",
"git_commit", "git_stash")`; a row outside them is dropped (fewer words, never a wrong one).

### §3.2 The hint and the forms

- `gate_brief.finding_door_hint(finding_id, options, paths, total, cap) -> list[str]`: the `answers` lines. When
  repository-writing options are among `options`: first `f"your uncommitted changes ({total}), all listed - commit and
  stash take exactly these:"`, then one line per path (`  - <path>`; a rename `  - <old> -> <new>`; paths as read
  from `-z`, never git's quoted form). When `total > cap`: instead `f"your uncommitted changes ({total}) are more than
  the {cap} this question can list, so I offer no commit or stash: commit or stash them yourself, then answer
  `{finding_id}: go on`"` and the first `cap` paths are NOT listed (only `total`). Then, per offered option in file
  order: `` `<id>: <word>` - <says> `` and its three price lines. `[]` when no option has a row.
- The finding gets a new key `answers` (list of str). Producer: `check_vcs` through `finding_door_hint`. Readers:
  `gate_preflight.render` (indented under `fix:`), `gate_preflight.brief_lines` (printed in full under the row, never
  clipped, and a row carrying `answers` is never cut by `limit`: `limit` counts the other rows), `gate_brief.render`
  (the cap at `:3868` grows by `len(answers lines)` as a bounded block, ≤ cap + 2 + 4×3 lines). `Rehearsal.add` takes
  `answers=` and replaces `DOOR_ID` in it as in `fix`. The `fix` becomes one line: "answer with one of the words listed
  under this item - " + `waiver_command(block)`; with no `answers` it is that sentence's plain fallback without words.
- `_finding_forms`: for every open line item, for every door option of its `waives` that has a `finding_door_words`
  row, one form `<item id>: <word>` (example `<real id>: <word>`, reader `Driver.read_finding_doors`, where "After
  your approval"), one form per word across items. Generic by capability: it also adds `product gap` (sibling of
  B-6, fork F16).

### §3.3 The stored shown doors (one writer, one reader; B-8)

- Writer: `gate_brief.keep_shown_doors(task_root, doors: dict, state: dict | None = None, gate: str = "A") -> None`.
  `state` given (the driver): `state.setdefault("shown_doors", {})[gate] = doors` (the driver saves its state as
  today). `state` None (the skill path): writes `state/driver-state.json` `shown_doors[gate]` under exactly the guards
  of `keep_shown_attachments` (folder exists; no current approved gate A decision; an existing file must be a JSON
  object, else no write). `doors = {finding id: waives}` for findings that carry `waives`.
- Callers: `Driver.gate` (`driver_gates.py:312-313`, replaces the two lines; B2) and `gate_brief.main`'s skill-path
  block, after the print, beside `keep_shown_attachments`, with the doors of `data["rehearsal"]` — the rehearsal that
  built the printed packet (B1). A failure prints one stderr line, never refuses the gate (as the attachments record).
- Reader: `gate_brief.shown_doors_of(task_root=None, state=None, gate="A") -> dict | None`: the stored dict, or None
  when absent, unreadable or not a dict. Readers: `_stand_gap_lines` (`:2793`, `state=self.state`; None reads as `{}`,
  today's direction) and `repo_words.main` (`task_root`).

### §3.4 The record (B-7; `waiver.py` unchanged)

`run` records nothing. It returns `done` with `block` (`vcs_state_block(head_after)`), `stage` (the shown door's own
`stage`, F-7) and `decision` = `person_decision(word, line, replaced)` + `"; done: <facts>; to undo: <undo text>"` +,
after a stash, `"; this word also passes a tree made dirty again at this HEAD"` (F-16). One builder of the argv,
`repo_words.record_args(task, done) -> list[str]` = `["--task", T, "--stage", S, "--block", B, "--decision", D]`.
- Driver: `self.py("waiver.py", *record_args(...), *self.waiver_road())` — the generic branch's own form.
- CLI: `subprocess.run([sys.executable, "-B", <scripts>/waiver.py, *record_args(...), "--by", by])` (an argv list, so
  `--decision` is not cut by cmd.exe; `person_words.read` refuses inline words only through `run-py.cmd`).
- When the write happened but the tree is still dirty (a hook, F-2): the record is `waiver.py --remark --task T
  --stage S --text <decision>` (words kept, NOTHING passed), so the next rehearsal asks again about what is left (I-2
  over I-5).

### §3.5 Git command forms (every form the body names; mark per DoD)

| id | form | mark |
|---|---|---|
| G1 | `git status --porcelain=v1 -z -uall` (rename as `XY new\0old\0`) | `-z`: ran by the critic (`g4`); `-uall`, space, non-ASCII, nested repository, ` A` under `-z`: **to run in B0-2** |
| G2 | `git rev-parse --git-path <MERGE_HEAD|CHERRY_PICK_HEAD|REVERT_HEAD|rebase-merge|rebase-apply|index.lock>` + exists | to run in B0-2 |
| G3 | `git ls-files -s -z -- <paths>` (mode `160000` = submodule) | to run in B0-2 |
| G4 | `git write-tree` before the add | to run in B0-2 |
| G5 | `git add -- <entries whose Y != ' ' or ??>` (skipped when empty) then `git commit -m MSG -- <every path, both rename sides, staged deletes>` | ran by the critic (`g4`: `D `,` M`,`R `,`??`); `MM`, space, non-ASCII, submodule, staged `qa-factory/` entry left out: to run in B0-2 |
| G6 | `git read-tree <tree>` (failure restore; undo after `git reset --soft <head_before>`) | to run in B0-2 |
| G7 | `git reset --soft <head12>` | `reset --soft HEAD~1` ran in B0; the abbreviated-sha form + G6: to run in B0-2 |
| G8 | `git stash push --include-untracked -m MSG -- <paths>` | ran in B0 (allowed classes); with the message builder's text: to run in B0-2 |
| G9 | `git rev-parse -q --verify refs/stash`; `git log -1 --format=%s <sha>` | to run in B0-2 |
| G10 | `git stash apply --index <sha12>`; `git stash drop <sha12>` (accepted or refused?); `git stash list --format="%H %gd %s"` | `pop --index` ran in B0; these forms: to run in B0-2 |
| G11 | `git rev-parse HEAD`; `git rev-parse HEAD^`; `git rev-parse --abbrev-ref HEAD` (detached prints `HEAD`); `git rev-parse --show-toplevel` | in the code today (`gate_preflight.py:228`, `:1929`, `:1933`); re-run for the record: to run in B0-2 |
| G12 | `git diff --name-status -z <head_before> HEAD` | B0 and the critic ran `git show --name-status HEAD`; this form: to run in B0-2 |
| G13 | `git log --fixed-strings --grep=<MSG> --format=%H -n 1` (the end reminder) | to run in B0-2 |

### §3.6 The executor's guard layers (B-4)

1. Per path, every entry's every path (both rename sides) lies outside the factory home read by
   `gate_preflight.factory_home_place(project_root, repo_dir) -> (rel, why)` (`why` ∈ `""`, `"outside"` = the home is
   not in this tree, `"unknown"` = cannot be told). `_factory_home_in_repo` becomes `return factory_home_place(...)[0]`
   (callers unchanged). `why == "unknown"` → refuse. A path under `rel` → refuse, naming it.
2. A path holding a separator the guard cuts at (` && `, ` || `, `;`, `\n`, ` | `) → refuse, naming it ("the guard
   cannot read this path whole").
3. `stage_guard.rule_pathspec(shlex.join(commit_argv))` and `rule_stash(shlex.join(stash_argv))`, each `-> str`, ""
   = pass. A non-empty answer stops the write with the guard's text (the guard used as a gate may err only toward
   refusing; adversarial inputs that must stay refused: a rename `qa-factory/x -> src/y`; a path `a;qa-factory/x`; a
   product path ending in `qa-factory` (F-15: refused by `_names_factory` — the safe side, the door names the guard
   text)). `rule_manifest` is not called: it takes `(ticket, what, event, *, required, pipeline, task_root)` and is
   vacuous before S5 (no manifest). `check_command` is not called (the orchestrator's Bash commands only).

### §3.7 The person's entries and the factory's (OW-2, one reader)

`gate_preflight.factory_origin(task_root, entries, top) -> dict[path, "factory" | "person"]` — THE one reader of "is
this path the factory's". Inputs: the S0 base (`test_repo_base.load`), the factory-writes record (format below; its
writer is fork F12 / node B6). Rules, in order:
1. A path in the S0 base `dirty` list → **person** (their change predates the story, even if a role rewrote it later).
2. A path whose current working-tree sha256 equals the LAST record row for it (rows `{"path": top-relative posix,
   "sha256", "at", "role"}` in `<task root>/state/factory-writes.jsonl`) → **factory**.
3. Everything else → **person**: no record, an unreadable record or line (the line is skipped), a sha mismatch (a hand
   edit after the factory's write), a deleted file (no current sha), a rename unless BOTH sides are factory.
Error direction: may say "person" for a factory file (it is shown and asked about; the allowed error); must never say
"factory" for a person's change. A truncated S0 base (`dirty_truncated`) changes nothing in rule 1's direction (a path
not kept is not proven the person's by the base, so rule 2 decides, and rule 3 stays the default).

`vcs_changes(project_root, config, task_root) -> dict | None`: `tests_root`, `branch`, `head`, `top`, `home`
(`factory_home_place`), `entries` (G1, factory home left out by the rule of `outside_factory_home` extracted as
`_in_home(path, home_rel)`), `person` and `factory` (by `factory_origin`), `digest = sha256` of the sorted
`"<xy>\0<path>\0<orig>"` of the PERSON's entries `[:12]`, `modes` (G3, for the stash blocker). None exactly where
`check_vcs` returns today.

`vcs_blockers(state) -> {"commit": [why], "stash": [why]}` (G2/G3 facts): both: an unmerged XY (`DD AU UD UA DU AA
UU`); an operation in progress; home `unknown`; a person path under the home or holding a guard separator; a nested
repository (`?? x/` under `-uall`); more than the cap; ` A` (intent-to-add) until B0-2 shows G4 handles it. Commit
only: detached HEAD. Stash only: X in `D R C`; a submodule (mode `160000`).

### §3.8 The reminder (OW-1)

One builder per moment, both in `repo_words`:
- `done_line(done) -> str` (right after): commit — "Your N uncommitted change(s) are now commit <sha12> on branch
  `<b>`, message "<msg>". To undo it: `git reset --soft <head12>`, then `git read-tree <tree12>`." stash — "Your N
  uncommitted change(s) are put aside in a git stash, "<msg>" (<sha12>). To take them back: `git stash apply --index
  <sha12>`, then drop that entry <drop form from B0-2>." Text passes `human_text.problems(..., kind="report")`;
  commands are the person's own tool, in backticks (human-questions.md).
- `reminder_line(project_root, config, task) -> str` (end of run): reads git, not prose: a stash entry whose subject
  carries `message(task, "stash")` still in the stash list (G10) → "Your changes from before the tests are still in
  the git stash "<msg>" (<sha12>): `git stash apply --index <sha12>` takes them back."; a commit whose subject is
  `message(task, "commit")` (G13) → "Before the tests, your changes were committed as <sha12> "<msg>" on branch
  `<b>`; they stay in its history."; neither (popped already, or nothing was done) → `""`. Git unreadable → `""` and
  one stderr line (a reminder never stops the end).
- `message(task, word) -> str` is the ONE builder of the commit/stash message (writer: `run`; reader: `reminder_line`).

Carriers. After the action — skill road: the CLI prints `done_line`; the conductor-actions row says "tell the person
the printed line as it stands". Driver road: `_relay_note` gains a section "## Done in the person's repository on
their word — tell the person each line as it stands" with the `done_line`s (fork F14 on whether that note reaches the
person when the gate passes). End of run — driver: at both terminal exits beside `give_back_config`, the line is
printed and appended to the done `Stop` text; skill: `s9.md:25` adds `repo_words.py --reminder --task <T>` (one JSON
line `{"line": ...}`), told as it stands.

---

## §4 Nodes

### §4.0 Order and ownership against part A

- Part A (t-105) owns `gate_preflight.check_open_questions`, `gate_brief.still_open`, a `question_register.py` helper,
  `tests/test_gate_preflight_question_status.py`, one `test-layers.json` row. **No node below owns any of these.**
- B1 shares `gate_preflight.py` (hot file) and `gate_brief.py` with part A, disjoint functions: **`очередь: A → B`**;
  B1 branches from `main` after t-105 is merged.
- **Wave 0: B0-2** (now; no package write). **Wave 1: B1** (after part A on `main` AND B0-2 accepted: B1's G1/G3/G2
  forms and blocker list depend on it) and **B6** (beside B1, disjoint files; only if F12 = (a)). **Wave 2: B2, B3**
  (B3 needs only the CLI name/flags fixed here). Then **B4** (Lead). **B5** queued.
- Owns are disjoint: B1 {vocabulary, gate_brief, gate_preflight, external_writes, test_gate_vocabulary,
  test_gate_question_form}; B2 {repo_words, driver_machine, driver_gates, judgment-census, test_gate_preflight,
  test_words_doors, driver-layers (conditional)}; B3 {s4.md, s9.md, conductor-actions, conductor.md, halts.md,
  state-exits.md, changelog fragment}; B6 {factory_writes, hooks.json, artifact-writers.json, test_guard_window_files,
  test_hooks_wiring}.

| wave | node | tier | needs |
|---|---|---|---|
| 0 | B0-2 measurement | builder | — |
| 1 | B1 data, reader, hint, change set, origin, store | builder | part A merged; B0-2 |
| 1 | B6 factory-writes record (F12 = a) | builder | F12 decided |
| 2 | B2 executor, driver road, census | builder | B1 |
| 2 | B3 skill road texts | builder | B1 (names), beside B2 |
| 3 | B4 map row | Lead | B1-B3 |
| — | B5 queued residual | — | a batch |

### B0 — done (t-110); its table is F0-23.

### B0-2 — wave-0 re-measurement of every form B0 and the critic did not run (no package write)

given: §3.5; `docs/tasks/specs/reports/t-110-b0-git-measure.md` (its `measure.py` is the model: fresh scratch repos,
`git -C`, `GIT_TERMINAL_PROMPT=0`, a dirty `qa-factory/` beside the listed paths).
owns: nothing in the repository (scratchpad only; the report path is given by the Lead's dispatch).
**Rows** (each: command, exit, stdout/stderr, porcelain before/after):
1. G1 on: `??` file, `??` folder with two files, a nested git repository, ` M`, `M `, `MM`, ` D`, `D `, `A `, ` A`
   (`git add -N`), `R `, a path with a space, a non-ASCII path, a rename one side under `qa-factory/`, a submodule —
   the raw `-z` bytes shown escaped.
2. G2 during a merge with a conflict, a rebase stopped on a conflict, a cherry-pick stopped; and after a killed commit.
3. G3 on the submodule and on a plain file.
4. G4 → G5 → G7 + G6 per class of row 1 that is not blocked (incl. `MM`, space, non-ASCII, ` A`, submodule), with a
   staged `qa-factory/x` that must stay staged and uncommitted: porcelain after the undo equals before? `git show :<mm>`.
5. G5 with a pre-commit hook exiting 1 on `MM`: then G6 restores `MM` and `git show :mm.txt`.
6. A pre-commit hook that rewrites a listed file; one that creates a new file: commit exit, porcelain after.
7. A pre-commit hook sleeping 200 s, the commit run with `subprocess.run(timeout=5)`: what is left (`index.lock`?
   HEAD?), then G6.
8. G8 with `MSG = message(T, "stash")`'s text per allowed class; G9 before/after; G10 apply `--index` by sha12 restores
   before-porcelain (`MM` included); `git stash drop <sha12>`: accepted or refused (verbatim).
9. G12 and G11 (`HEAD^`, detached `--abbrev-ref`), G13 on a commit with MSG.
DoD: the table per row, the git version, the verbatim output, the full script source attached. The Lead copies the
results into §0 as F0-32 and lifts or keeps each blocker of §3.7 accordingly (a class lifted only on a row that shows
exact take + true undo).

### B1 — data, reader, hint, forms, change set, origin, shown-doors store (wave 1)

given: this spec; `ai-packages/qa-factory/design/factory-rules.md` (whole); `plans/builder-rules.md`; B0-2's report.
owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\question-vocabulary.json` (block `finding_door_words` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_brief.py` (`FINDING_DOOR_OPTIONS`, new `FINDING_DOOR_EXECUTORS`, `finding_door_words`, `finding_door_option`, `finding_door_word_of`, new `finding_door_hint`, `_finding_forms`, `render` (the cap line only), new `keep_shown_doors`, new `shown_doors_of`, `main` (skill-path block only))
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\gate_preflight.py` (`check_vcs`, `Rehearsal.add` (the `answers` kwarg only), new `vcs_state_block`, new `vcs_changes`, new `vcs_blockers`, new `factory_home_place`, `_factory_home_in_repo`, `outside_factory_home` (rule extracted to new `_in_home`), new `factory_origin`, new constant `REPO_WORD_PATH_CAP`, `render`, `brief_lines`; NOT `check_open_questions`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\external_writes.py` (`closed_by_run`: new keyword `unreadable_closes=False`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_vocabulary.py` (one new part beside `part_stand_gap_words`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_question_form.py` (rows/parts named below)
non-goals: the executor; the driver; texts of roles; the clean-tree literal and `check_stand` (B5); any quarantined test.
handoff: the diff, the FR pass (§7), the witness output, AR rows touched.

**Behaviour**
1. §3.1 rows; `finding_door_words` returns `executor`, `writes_repository` (default false), price lines (default "").
2. `finding_door_option`: a `writes_repository` row is read only as the word or a synonym ALONE; anything after it →
   `("", "")`. Other rows keep today's rule.
3. `external_writes.closed_by_run(task_root, unreadable_closes=False)`: with `True`, a pipeline that cannot be read or
   is not an object returns "the run's record cannot be read, so nothing is written into your repository". Default
   keeps every other caller byte-identical.
4. `factory_home_place`, `_in_home`, `vcs_changes`, `vcs_blockers`, `factory_origin`, `vcs_state_block` per §3.3/§3.7.
5. `check_vcs` rewritten on `vcs_changes` (no second status read): dirty = the PERSON's entries.
   - Person's entries present: message as today over the person's entries (paths from `-z`), plus, when factory
     entries exist, the clause `" (the factory's own N file(s) of this story are not counted)"`. Doors: `accept`
     (HEAD block, as today); `go on` (`door(block, option="vcs_go_on")`); and `commit`/`stash` on
     `f"test repository changes: {head[:12]} {digest}"` each only when ALL hold: `closed_by_run(task_root,
     unreadable_closes=True)` is falsy, `len(person) <= REPO_WORD_PATH_CAP`, `vcs_blockers` names nothing for that
     word. `fix` and `answers` per §3.2.
   - Only factory entries: no dirty finding; the clean-branch finding as today (B5 owns its literal), plus one `info`
     row (check `vcs`, rendered in INFO, never a question): "the test repository holds only files this story's
     factory roles wrote (N): <first 5> - nothing of yours is uncommitted" (fork F13).
   - No entries: as today.
6. `render`: a multi-line `fix`/`answers` is indented (continuation 10 spaces); a one-line `fix` byte-identical.
   `brief_lines`: a row with `answers` prints them in full under it and is never cut by `limit`.
7. `gate_brief.render`: the cap grows by the `answers` lines of the rehearsal's rows (bounded).
8. `_finding_forms` per §3.2. `keep_shown_doors` / `shown_doors_of` per §3.3; `main` calls the writer on the skill path.

**Edges**

| Edge | Behaviour | Invariant |
|---|---|---|
| Vocabulary unreadable / block missing | Only `accept`; plain-words `fix`; no `answers` words | I-1, AR-28 |
| Damaged row | Dropped | I-1 |
| No HEAD | No door at all (as today); no words | I-2 |
| No-trace run / pipeline unreadable | Only `go on` + `accept`; the hint names only `go on` | I-7 |
| Person's entries = 20 (cap met) | All 20 listed; commit/stash offered | I-2 |
| 21 (cap + 1) | None listed by path; the over-cap sentence; only `go on` + `accept` | I-2: no write on an unshown path |
| A path with a space / `café.txt` | Read from `-z`, listed and digested as the real path, never git's quoted text | I-2 |
| An untracked folder | Listed file by file (`-uall`); a new file in it changes the digest (F-1) | I-2 |
| A nested repository `?? x/` | Listed as the person's; commit/stash not offered (`vcs_blockers`) | I-1 |
| Unmerged entry / merge, rebase, cherry-pick in progress | Listed; commit/stash not offered | I-1, I-8 |
| Detached HEAD | Commit not offered; stash and go on stand | I-1 (F-8) |
| Staged `D`/`R`/`C` or a submodule | Stash not offered; commit stands | I-1 (B0) |
| Home `unknown` | Commit/stash not offered | I-2 |
| A rename with one side under `qa-factory/` | Listed (person's), commit/stash not offered | I-2 (B-4) |
| First run, no factory record | Every entry the person's (today's behaviour) | I-9 |
| Re-run / rework after S5: factory files with matching record rows | Not counted; the clause names their number | OW-2, I-9 |
| A file in the S0 base, rewritten by a role | The person's | I-9 |
| A factory file the person edited by hand | sha mismatch → the person's (listed, taken by commit/stash) | I-9 (owner) |
| Record unreadable, a bad line | That line skipped / all person's; the info row says "the record of the factory's own files could not be read; every change is shown as yours" | I-9, FR-59 |
| Only factory entries | No question; one info line | OW-2, F13 |
| The tree changes between packet and answer | Digest differs from the stored door → the driver leaves the line unread; the CLI refuses (B2) | I-2 |
| Skill path: story folder absent / gate A decided / state file not an object | `keep_shown_doors` writes nothing (the CLI then refuses: B2) | I-2 |

**Tests** (rows in keep files; each green and red on revert of its item, stated by the builder)
- `test_gate_vocabulary.py` new `part_finding_door_words`: the four rows with executors; ASCII; disjoint from every
  block and `gate-approval-words.json`; damaged rows dropped; `finding_door_option` table — read: `commit`, `COMMIT`,
  `` `commit` ``, `commit.`, `  commit  `, `stash them`, `go on`, `Go On!`, `go on` with an NBSP (read: `str.split`
  folds it — intended), `go on, the branch is mine`; not read: `commit or stash`, `commit please`, `stash, then go on`,
  `commits`, `go onward`, Cyrillic `коммит` and the homoglyph `сommit` (U+0441) built from code points, full-width
  `ｃｏｍｍｉｔ` from code points, `""`, `"   "`, `commit\u200b`, and a 1001-character line starting with `commit`
  (labelled "magnitude; no limit exists in the reader").
- `test_gate_question_form.py`:
  - a dirty `vcs-test-repo` finding (doors `accept`, `vcs_go_on`, `vcs_commit`, `vcs_stash`): each `vcs-test-repo:
    commit|stash|go on`, `- \`vcs-test-repo\`: commit` read by `Driver.read_finding_doors` with its option; `maybe`
    read by none; two lines `commit` then `commit?` → both unread (the last is a question, the earlier set aside).
  - `answer_forms` lists `<item id>: commit|stash|go on` (and `product gap` for a product-gap item) and each example
    is read (the existing reader-table row).
  - `answers` pass `human_text.problems`; three price lines per word; `brief_lines` prints them for a row placed
    7th of 7; `gate_brief.render` keeps them under a 40-line cover sheet.
  - `check_vcs` on a temp repo (`git init`, `M`/`??` plain paths, no factory files): `message` and the `accept` door
    byte-equal to a literal captured from today's code in the same test.
  - cap table: 20 person entries → commit/stash doors present, all 20 paths in `answers`; 21 → absent, the over-cap
    sentence, no path lines.
  - a no-trace pipeline and an unreadable `pipeline.json` → no commit/stash door; `commit` unread.
  - `factory_origin` table on a temp repo + S0 base + record: no record → person; matching row → factory; edited
    after → person; in S0 base and in the record → person; bad JSON line → skipped; rename half factory → person;
    deleted → person. And `check_vcs` with only factory entries → no dirty finding, the info row.
  - `keep_shown_doors`/`shown_doors_of`: driver form (state dict), skill form (file), the three no-write guards,
    unreadable → None.

**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/references/question-vocabulary.json ai-packages/qa-factory/scripts/gate_brief.py ai-packages/qa-factory/scripts/gate_preflight.py ai-packages/qa-factory/scripts/external_writes.py`
— run what it prints, plus `python -B ai-packages/qa-factory/scripts/tests/test_judgment_census.py` (expect no change:
no new function matches `UNIT_NAME_RE`) and `python -B ai-packages/qa-factory/scripts/selftest.py --lang`. AR-1 grep as
§1. AR rows touched: AR-1, 9, 13, 16, 22, 28.

### B2 — the executor, the driver road, the census (wave 2)

given: this spec; `factory-rules.md`; `plans/builder-rules.md`; B0-2's report; B1 on `main`.
owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\repo_words.py` (new: `run`, `message`, `record_args`, `done_line`, `reminder_line`, `main`; no other function may match `UNIT_NAME_RE`, no `raise ValueError`/`StateConflict`, no `deny`/`block`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_machine.py` (`_record_door_lines`, `_relay_note`, `_stand_gap_lines` (the `:2793` read only), the two terminal exits at `:1375-1378` and `:1938-1940` (the reminder only))
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\driver_gates.py` (`gate`, lines `:312-313` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\judgment-census.json` (one row; `ratchet.safety`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_gate_preflight.py` (one new part function)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_words_doors.py` (one row: the CLI)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\fixtures\driver-layers.json` (only if its census demands it; named in the report)
non-goals: `waiver.py`; texts; B1's functions; any quarantined test.
handoff: the diff, the FR pass, witness output, the census raise named.

**`repo_words.run(task_root, project_root, config, option, line, replaced, door) -> (done: dict, problem: str)`** —
`door` is the SHOWN door (`{block, stage, option}`): driver `entry["door"]`, CLI the stored one.
1. `option` → row; executor `git_commit`/`git_stash`, else problem "not a repository word".
2. `closed_by_run(task_root, unreadable_closes=True)` truthy → problem with door "answer `vcs-test-repo: go on`, or
   commit/stash yourself and answer `go on`".
3. `state = vcs_changes(...)`: None → "the test repository could not be read by git"; `state["person"] == []` →
   "nothing of yours is uncommitted now; nothing was done" (no record); `f"test repository changes: {head12}
   {digest}" != door["block"]` → "your repository changed since you were shown the list; nothing was done".
4. `vcs_blockers(state)[word]` non-empty → problem naming the first reason and the paths, door "commit or stash it
   yourself, then answer `vcs-test-repo: go on`". Then the three guard layers of §3.6.
5. `before = {head, stash_ref (G9), tree (G4, commit only)}`. G4 failing → problem, nothing written.
6. Run (cwd `top`, `_git`'s env, `REPO_WORD_TIMEOUT = 120` s, no `--no-verify`, no `-c`): commit = G5 with `MSG =
   message(task, "commit")`; stash = G8 with `message(task, "stash")`.
7. Judge on the state, never the exit code alone (`after = vcs_changes(...)`, G11, G9, G12):
   - commit DONE: HEAD moved, `HEAD^ == head_before`, the G12 path set == the person's paths, `after["person"] == []`.
   - stash DONE: `refs/stash` changed to a sha whose subject carries MSG, `after["person"] == []`.
   - Done but `after["person"]` not empty (a hook rewrote/created files) → `done` with `still = [paths]`, plus problem
     "the commit IS made (<facts>); these are still uncommitted: <paths>" — the caller records a REMARK (§3.4).
   - Not done after `git add` → restore `git read-tree <tree>` (G6), never `git reset -- <paths>`; problem = git's
     stderr (last 600 chars) + "nothing is passed; the question stays open" (+ "restoring what you had staged failed:
     <text>; `git read-tree <tree12>` restores it" if G6 fails).
   - Stash ref changed on a non-zero exit → problem "a stash entry was left: <sha12>; your tree is <unchanged | these
     changed: …>"; never dropped, never a pass.
   - Timeout: no retry; judge 7 again on the state (a commit that landed is DONE); otherwise G2 `index.lock` exists →
     problem "the command did not finish in 120 s; HEAD is <x> (was <y>); a leftover `.git/index.lock` blocks git: if
     no git is running, delete it, then `git read-tree <tree12>` restores what you had staged" (the factory never
     deletes a lock); no lock → G6 then the problem.
8. `done = {word, head_before, head_after, tree, stash_sha, paths: N, block, stage: door["stage"], decision, undo,
   still}` (§3.4, §3.8).

**`main`**: `repo_words.py --task <T> --word <word> --words-file <file> [--by <who>]` and `--reminder --task <T>`.
- `--word` maps the vocabulary WORD to its option via `finding_door_words` (AR-1).
- `shown_doors_of(task_root)`: None → exit 3, "what gate A showed cannot be read; nothing was done; show gate A again
  (`gate_brief.py --task <T> --gate A`) and ask the person". The stored doors are searched for the ONE door with that
  option (no id literal): none → exit 2 "the question you were shown does not offer that word"; two → exit 2.
- The words file (`person_words.read`) must read as the exact word (fork F9 (a)): a line `<that finding's id>:
  <rest>` matched by the driver's `_FINDING_LINE_RE` (imported lazily from `driver_machine`) whose `rest` reads
  through `finding_door_option` as the option, or the whole text reading so; the last such line; a `?` → exit 2 "the
  person's answer is not the exact word; ask them once to answer `<id>: <word>`".
- `run`, then record via `waiver.py` with `record_args` + `--by` (default `human`); print `done_line` (exit 0), or the
  problem with `person_words.door(...)` (exit 3). Record failed after a write → exit 3 "the commit/stash IS made
  (<facts>); only the record of the person's word failed: <text>" + the record command.
- `--reminder`: prints `json.dumps({"line": reminder_line(...)})`, exit 0 always.

**Driver changes**
- `_record_door_lines`: dispatch every branch on the row's `executor` (F-12): `product_gap` → today's branch; `record`
  → today's generic waiver branch; `git_commit`/`git_stash` → `repo_words.run(..., door=entry["door"])`; problem →
  `failed.append((id, line, problem))`; done → record with `record_args` + `waiver_road()` (a remark when `still`),
  `recorded.append`, print `done_line`, keep it for the note.
- `_relay_note`: the done lines (§3.8 section); each finding door shows its word: `word option vcs_commit (\`commit\`)`.
- `_stand_gap_lines` `:2793`: `gate_brief.shown_doors_of(state=self.state, gate=gate)`.
- `Driver.gate` `:312-313`: `gate_brief.keep_shown_doors(self.task_root, doors, state=self.state, gate=gate)`.
- Terminal exits: `reminder_line` printed; at `:1378` appended to the Stop text.

**Census (B-10, AR-20)**: add `{"file": "repo_words.py", "function": "run", "class": "safety", "roles":
["conductor"], "owner": "intent"}`; `ratchet.safety` 54 → 55 (this row only). `breach`, `blocks_overrides`,
`blocking_per_role`, `word-list`, `meaning-proxy`, `meaning`: unchanged (`run` is not on the blocking path and calls no
`deny`).

**Edges**

| Edge | Behaviour | Invariant |
|---|---|---|
| Empty change set at execution | "nothing of yours is uncommitted now"; no git write, no record | I-6 (no record of an action that did not happen) |
| Stored shown block absent/unreadable (CLI) | exit 3, nothing run, door "show gate A again" | I-2 on the skill road |
| Stored block differs from fresh digest | refused, nothing run | I-2 |
| Cap exceeded at execution (an old door) | `vcs_blockers` refuses | I-2 |
| Space / non-ASCII path | argv carries the `-z` path; G5/G8 per B0 unquoted rows | I-2 |
| `MM` on commit | G5 commits the worktree content (B0 class 5); the index split stays in `tree`; undo restores `MM` (B0-2 row 4) | I-8 |
| `MM` on stash | G8; undo `apply --index` restores `MM` (B0 `pop --index`, B0-2 row 8) | I-8 |
| Hook refuses (exit 1) | G6 restores the index (`MM` kept); problem; no record | I-4, I-6, I-8 |
| Hook rewrites files | DONE + `still`; remark, no pass; the next rehearsal asks about what is left | I-2 over I-5 |
| Timeout mid-commit | state judged; `index.lock` named, never deleted; no retry | I-6, I-8 |
| Stash 128 with an entry left | named by sha, never dropped, no pass | I-6, I-8 |
| Two lines commit/stash | last wins (existing); `replaced` in the record | I-3 |
| `commit please` / other words / another language | unread → the conductor asks for the exact word (B3) | I-3 |
| Dry run | nothing read (existing `:2515`) | I-3 |
| Record fails after a write | the action is told as made; the conductor records it | I-6 |
| tests_root in the product repository | product changes are the person's and are taken; `says` names "product code included" (Q-1) | I-2 |

**Tests** (`test_gate_preflight.py`, new part `part_repo_words`, one temp git repo + seeded task root, a case per line;
the CLI row in `test_words_doors.py`)
- commit: HEAD moves, the person's paths committed, `qa-factory/` and a factory file stay dirty, the waiver on the new
  block with the line quoted and the undo named; next `check_vcs`: no `vcs-test-repo`; undo then porcelain == before
  (`MM` included).
- stash: tree clean of the person's entries, stash subject = `message`, waiver on HEAD; undo == before.
- go on: waiver only. Stale digest, no-trace, unreadable pipeline, blocker per class, `qa-factory` rename, `;` path:
  refused with their doors, nothing written (porcelain and `refs/stash` unchanged).
- pre-commit hook exit 1 on `MM`: porcelain `MM`, `git show :mm` as before, no waiver. Hook that rewrites: remark,
  no waiver, problem names the path.
- built argv passes `rule_pathspec`/`rule_stash`.
- driver: `_record_door_lines` with a `vcs_commit` entry calls `run` (stubbed) and records via `record_args`; a
  `product_gap` entry keeps its branch.
- `reminder_line`: stash present → the line; popped → ""; commit with MSG → the commit line.
- `test_words_doors.py`: the CLI takes `--words-file` and prints `door()` on refusal; a words file `commit please` →
  exit 2.

**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/repo_words.py ai-packages/qa-factory/scripts/driver_machine.py ai-packages/qa-factory/scripts/driver_gates.py ai-packages/qa-factory/scripts/tests/fixtures/judgment-census.json`
— run what it prints, plus `test_judgment_census.py` and `test_state_exits.py` if not printed. The `safety` raise is
named. AR rows: AR-9, 13, 14, 15, 17, 19, 20, 24, 25, 28, 29.

### B3 — the skill road and the conductor's texts (wave 2, beside B2)

given: this spec; `factory-rules.md`; `plans/builder-rules.md`.
owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s4.md` (the paragraph at `:159-163` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\skills\qa-story\phases\s9.md` (the sentence at `:25` only)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor-actions.json` (one new row after the `product_gaps.py record` row)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\conductor.md` (the row at `:21`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\halts.md` (the row at `:19`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\design\state-exits.md` (two new rows)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\changelog.d\fg7-8-b-vcs-words.md` (new fragment)
non-goals: code; B5's evals.
handoff: the diff, the witness output.

**Behaviour**
- `s4.md` (one sentence, replacing nothing else): the test-repository item's own words (`commit`, `stash`, `go on`,
  listed under it) are carried out by their conductor-actions row only when the person's answer IS that word
  (`vcs-test-repo: commit` or `commit` alone); any other wording, a condition or a question: ask the person once to
  answer with the exact word, and run nothing until they do. Tell the line the command prints as it stands.
- conductor-actions row: says "the person answered the test-repository item with exactly `commit` or `stash`"; run
  `repo_words.py --task <T> --word <word> --words-file <file with their exact answer>`, once; a refusal is told in
  words, nothing else runs; the printed line is told to the person as it stands. `go on`: `waiver.py --task <T>
  --stage S5 --block "<the item's block>" --words-file <file>`.
- `conductor.md:21` names the row and the exact-word rule (I-3), and "the driver's note section 'Done in the person's
  repository' is told to the person line by line".
- `s9.md:25`: after `config-restore`, run `repo_words.py --reminder --task <T>`; a non-empty `line` is told as it stands.
- `halts.md:19`: the dirty tree is a gate A item whose words are the item's own; the four literal words removed.
- `state-exits.md`: "changes committed on the person's word at gate A" → `git reset --soft <head_before>` then `git
  read-tree <tree>` (the person's, named in the record); "changes stashed on the person's word at gate A" → `git stash
  apply --index <sha>` then drop that entry (the B0-2 form); both with F-16's sentence for the stash.
- Changelog: one paragraph.

**Edges:** other words → ask once, never run (I-3); the person answers the exact word → run once (I-3); the CLI refuses
→ tell it, run nothing else (I-6).
**Tests:** none new; the witness runs what `--witness-for` prints (`test_words_doors.py` (a) scan: the row uses
`--words-file`).
**DoD:** `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/skills/qa-story/phases/s4.md ai-packages/qa-factory/skills/qa-story/phases/s9.md ai-packages/qa-factory/references/conductor-actions.json ai-packages/qa-factory/references/conductor.md ai-packages/qa-factory/references/halts.md ai-packages/qa-factory/design/state-exits.md`
plus `selftest.py --lang` and `role_load.py --all` before/after. AR rows: AR-17, 19, 25.

### B4 — the Lead: the map row

owns: `C:\QAFactory\forge-repo\docs\SIBLING_MAP.md` (axis 5, one row "Gate A test-repository words"): data
`finding_door_words`; reader `finding_door_words`/`finding_door_option`; hint `finding_door_hint` (`answers`); forms
`_finding_forms`; door `check_vcs`; store/reader `keep_shown_doors`/`shown_doors_of`; executor `repo_words.run`; driver
`_record_door_lines`; skill road `s4.md` + conductor-actions row + `conductor.md:21`; reminder `done_line`/
`reminder_line`; origin `factory_origin`. DoD: the row present; axis 34 holds (one executor, one store, two roads).

### B5 — queued residual (F6 + one found here)

owns (when taken): `gate_preflight.py` (`check_vcs` clean branch, `check_stand`, `brief_lines`' "+N more … under
Rehearsal of gate A below" sentence, which the skill road's message has no section for — F0-25), `question-vocabulary.json`,
`skills/qa-story/evals/evals.json` (`:53`, `:64`), `evals/plugin-eval-benchmark.json` (`:86-93`). Test: rows in
`test_gate_question_form.py`. The Lead files it as a finding into an untaken batch of the pile.

### B6 — the record of files the factory wrote (only if F12 = (a); wave 1)

given: §3.7 (the record format); `hooks/hooks.json`; `window_files.py` (the guard's write-path idioms).
owns:
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\factory_writes.py` (new: `record(task_root, rel, sha256, role)` — THE writer of `state/factory-writes.jsonl`, append-only; `main` — the PostToolUse hook)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\hooks\hooks.json` (one entry in the `Write|Edit` PostToolUse matcher, after `validate_artifacts.py`)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\references\artifact-writers.json` (one row)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_guard_window_files.py` (one part)
- `C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_hooks_wiring.py` (one row)
Behaviour: on a Write/Edit by a session bound to a running story's role dispatch (resolved as `guard_pre_tool`
resolves the story for `window_file_check` — not verified, the builder names the function), of a file inside the
project and outside the factory home, append `{path (top-relative posix), sha256 of the bytes now, at, role}`. Any
failure: no row, exit 0, one stderr line (a missing row only makes the file read as the person's — the safe side).
Writes by Bash (generators) are not seen: such files read as the person's (allowed error). Edges: two writes of one
file → two rows, the last counts (rework); a write by the orchestrator in the person's chat → recorded as the
factory's (it wrote it; fork F12 note). Tests: a hook event for a role write appends a row; outside the project, under
`qa-factory/`, no story → no row; a broken record directory → exit 0, no row.
DoD: `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/factory_writes.py ai-packages/qa-factory/hooks/hooks.json ai-packages/qa-factory/references/artifact-writers.json`
plus `test_artifact_writers.py`, `test_judgment_census.py`. The hook file is handed over by the builder; the Lead
places the `hooks.json` entry at acceptance (enforcement-file rule). AR rows: AR-12 (one append per write, measured),
AR-14, AR-22, AR-28.

---

## §5 Forks

Decided earlier: F1 (a), F2 (a), F3 (a) (owner: not in the report — OW-1), F4–F7 (a); B-8 (a) (Lead, t-115).

| id | Fork | Options and consequences | Recommendation |
|---|---|---|---|
| **Q-1** (owner) | F-14: "product code included" | When tests live in the product repository, `commit`/`stash` take the person's product work-in-progress too, under a factory-written message. (a) allowed, `says` names it; (b) offer commit/stash only when every person entry lies under `tests_root`. | Lead takes it to the owner with F1; until then (a), marked "until the owner's word". |
| F9 | The CLI checks the words file holds the exact word | (a) yes, through `finding_door_option` and the driver's line pattern: I-3 is code-held on the skill road too; cost: a lazy import of `driver_machine`, a refusal when the conductor passes a summary. (b) discipline only (the s4 sentence). | (a) |
| F10 | The path cap | 20 paths: a person checks 20 lines at a glance; the packet grows by ≤ 34 lines, a bounded block. Lower (10) refuses more trees; higher makes the list unread. | 20 |
| F11 | The commit undo rests on an unreferenced tree object | git prunes unreferenced objects after its `gc.pruneExpire` (two weeks by default — estimate, not verified). (a) the undo text says "valid for about two weeks"; (b) keep it reachable with a ref `refs/qa-factory/<task>/index-before` — a second write into the person's repository. | (a) |
| F12 | The carrier of "the factory wrote this file" (OW-2) | No carrier holds it today (F0-30). (a) a new append-only record `state/factory-writes.jsonl` with the sha after each role Write/Edit (node B6; a hook on every write, AR-12 cost: one append). (b) `automation-manifest.json` `tests[].file` plus the S0 base, no hashes: helpers unseen (shown as the person's — safe), but a hand-edited factory test would read as the factory's and be hidden — breaks the owner's "edited by hand is the person's". (c) none: everything stays the person's (today). | (a); B1's reader works in both worlds — until B6 lands there is no record and every entry is the person's (today's behaviour, never the unsafe side). |
| F13 | Tree dirty only with the factory's files | (a) no question, one info line, the clean-branch question as today; (b) the dirty question anyway with a note. | (a) |
| F14 | The after-action line on the driver road | (a) a section of `_relay_note` the conductor tells line by line (not verified that the note reaches the conductor when the gate passes cleanly); (b) a stored line shown at the person's next stop (`gate_note`-like). | (a); B2 states in its report whether the note is delivered on a clean pass, (b) opens as a node if not. |
| F15 | F-5: `accept <reason>` and `go on` pass the same block | (a) keep both: `accept` is the universal door (FR-4), `go on` the item's own word, no reason; the hint says `go on`; (b) drop `go on`. | (a) |
| F16 | `_finding_forms` generic rule also lists `product gap` | (a) in B1 (one rule by capability, P31); (b) queue to B5. | (a) |

### Small choices closed by the designer
- Module `repo_words.py`; options `vcs_commit|vcs_stash|vcs_go_on`; executors `record|git_commit|git_stash`.
- Digest: sha256 of the sorted `xy\0path\0orig` of the person's entries, 12 hex; block ≤ 60 chars (50).
- `REPO_WORD_TIMEOUT = 120` s; no retry.
- Paths are shown without status codes (no jargon; human-questions.md).
- `render` (`--text`) prints `answers` too: on the driver road the list appears in the brief and in the rehearsal
  section (F-13: longer, never contradicting).
- The message line of the dirty finding is built from the `-z` read (one read, AR-13): byte-identical to today only
  without folders and quoted paths; the test row uses plain paths.
- The CLI finds its door by option, never by the id literal.

---

## §6 Not verified

- Every G-form marked "to run in B0-2" (§3.5).
- Whether `_relay_note`'s note reaches the conductor when the gate passes with nothing unread (F14).
- How `guard_pre_tool` resolves the running story and the role for a write (B6).
- That `state/driver-state.json` is saved before the driver hands a held line to the conductor (the CLI reads the file).
- `git gc` prune window for the undo tree (F11).
- Whether `test_gate_preflight.py`'s harness is quick enough for a temp-repo part; if not, B2 names the fallback keep
  file in its report (never a new file).
- Whether `fixtures/driver-layers.json` needs a row for the changed driver methods.
- Stash against `test_novelty` (F-9): a test file dirty at S0 and stashed may read `dirty_changed`/lost
  (`test_novelty.py:268-279`, `544-559`, by the critic's reading). Not run; stash takes only the person's entries, and a
  test file dirty at S0 is the person's — B0-2 does not cover it; it stays a known risk named in the record.

---

## §7 FR pass (A–C)

- **A.** FR-1/2: every problem says what, what was expected, and a door (person: commit/stash yourself, then `go on`;
  conductor: the command). FR-3: failures reported, the person not asked to resend. FR-4: `go on`/`accept`. FR-46:
  git refused = the story's; stale door = the call's. FR-48: the conductor gets the failed line once. FR-57: hooks run,
  the guard asked, no override. FR-59: an unknown origin is the person's; unknown home/pipeline offers no write.
- **B.** FR-6: `answers` through human-questions (rule 4 closed set, rule 6 prices, commands as the person's own tool).
  FR-7: no re-ask after a clean commit/stash; re-ask only when I-2 demands. FR-8/9: the line reaches one executor,
  every offered word has one. FR-10: the forms list, the `answers` and the `fix` say the same words (B-6).
- **C.** FR-11: the conductor-actions row names an existing command. FR-12: no phrase list; other words go back to
  the person. FR-13: words and executors in data. FR-14: the CLI prints one line or a problem with a door. FR-15: the
  conductor is given the command. FR-38: the block the next rehearsal checks is the one recorded. FR-42: every state
  `run` returns has a move. FR-45: `factory_writes` is a recorder, not the validator.
- D–G: FR-30 (ASCII data, Cyrillic test inputs from code points), FR-32 (rows).

---

## §8 Reading trail (t-115 additions; t-106's trail stands)

- Read whole: the spec; `reviews/t-109-fg7-8-b-plan.md`; `reports/t-110-b0-git-measure.md`.
- `gate_preflight.py`: 205-264, 1910-1959, 5787-5821, 5917-5992, 6081-6098; Grep `def (outside_factory_home|...)`,
  `LIST_LIMIT|BRIEF_CUT`.
- `gate_brief.py`: 405-574, 2840-3069, 3320-3410, 3850-3882, 5061-5110; Grep `MAX_LINES`, `ATTACHMENTS_STATE_FILE`,
  `_FORM_LINE_RE`.
- `driver_gates.py`: 90-140, 280-330. `driver_machine.py`: 2765-2879, 2908-2969, 3078-3187; Grep `give_back_config`,
  `_FINDING_LINE_RE`. `driver_runner.py`: 203-225, 321-335, 1258-1287. `driver_core.py`: Grep `driver-state.json`.
- `waiver.py`: 984-1044, 1566-1659. `person_words.py`: 110-199. `person_owned.py`: Grep `driver`.
- `stage_guard.py`: 2318-2442. `external_writes.py`: 185-206. `test_repo_base.py`: 1-120. `test_novelty.py`: Grep `^def`.
- `window_files.py`: 1-90. `activity_capture.py`: 1-40. `contract.py`: 3773-3792. `proof_level.py`: 519-531.
  `handoff_check.py`: 440-470. `story_step.py`: Grep `config-restore|give_back_config`, 863-885.
- `hooks/hooks.json`: Grep `PostToolUse|command`, 55-79.
- `skills/qa-story/phases/s4.md`: 120-169, 196-220; `s8.md`: 378-402; `s9.md`: Grep.
- `tests/test_judgment_census.py`: 1-90, 175-266, Grep. `fixtures/judgment-census.json`: 1-20, Grep rows.
  `tests/test-layers.json`: Grep section heads and file rows.
- Greps with positive controls: `shown_doors` (hits); `_factory_home_in_repo|outside_factory_home` (hits);
  `option="product_gap"|"product_gap"` (hits); `walk.claim|files-written|...` -i (hits in other files);
  `sha256|home_hash|SHA256` -i in `manifest_put.py` (16 hits, `home_hash` only — the negative "no whole-file hash per
  test row" rests on that, not verified beyond it); `SLOW_TESTS\s*=` (no hit; no control run — not used as a claim).
- Needed beyond the manifest: everything after the three given files above (the revision had to re-read the carriers).

---

## §9 Revision after t-109

| Finding | Where resolved / the fork it became |
|---|---|
| B-1 command form, class handling | §3.5 G1/G5/G8, §3.7 `vcs_blockers`, B2 steps 4-7 (post-state success; stash ref changed on non-zero named); B0-2 rows 1-4, 8 |
| B-2 undo text | §3.4, §3.8, B2 step 8, B3 `state-exits.md`: `reset --soft` + `read-tree <tree>`; `stash apply --index <sha>` + drop (B0-2 row 8); test rows "undo == before"; F11 |
| B-3 failure path | B2 step 7: `git read-tree <tree>` (G4/G6), never `reset -- paths`; test row `MM` + hook exit 1 |
| B-4 factory folder | §3.6 layers 1-3; `factory_home_place`; `rule_manifest` dropped with its reason; AR-15 row rewritten |
| B-5 more than five paths | §3.2 `answers` lists every path; cap 20 (F10); over the cap only `go on`/`accept`; printed on both roads (F0-25: `brief_lines` + `gate_brief.render` cap) |
| B-6 forms list | B1 owns `_finding_forms`; §3.2; F16 for `product gap` |
| B-7 waiver call | §3.4: `run` returns facts, callers record with `--decision` through `record_args`; remark when the tree stays dirty; `waiver.py` unchanged |
| B-8 skill-road shown state | §3.3 one writer `keep_shown_doors`, one reader `shown_doors_of`, same key/file on both roads; CLI compares against the stored door |
| B-9 I-3 vs B3 | I-3 rewritten; B3 `s4.md`/conductor-actions/conductor.md: ask once for the exact word; F9 (code check of the words file) |
| B-10 census | B2 owns `judgment-census.json`; row + `safety` 54 → 55, others unchanged |
| F-1 digest pins entries | `-uall` per file (G1); content edits by the person between show and answer are not pinned (a new/removed file or a status change is) — stated; B1 edge |
| F-2 hook-dirtied tree | B2 step 7 `still` + remark, no pass; I-5 yields to I-2 |
| F-3 timeout, `index.lock` | B2 step 7 timeout branch; never deleted by the factory; B0-2 row 7 |
| F-4 unreadable pipeline | `closed_by_run(..., unreadable_closes=True)` in `check_vcs` and `run`; other callers unchanged |
| F-5 accept vs go on | F15 |
| F-6 undo text a person reads | §3.8 through `human_text.problems`, commands in backticks |
| F-7 `--stage S5` literal | the shown door's `stage` (§3.4) |
| F-8 detached HEAD | commit blocker (§3.7), not offered |
| F-9 stash vs `test_novelty` | §6, a named risk |
| F-10 battery additions | B1 `part_finding_door_words` and the `commit` / `commit?` row |
| F-11 test placement | git table in `test_gate_preflight.py` (keep, B2); only the CLI row in `test_words_doors.py` |
| F-12 dispatch style | `_record_door_lines` dispatches every branch on `executor` |
| F-13 packet length | `answers` bounded (≤ cap + 14 lines), counted in the cover cap; duplicated on the driver road — small choice |
| F-14 product code | Q-1 (owner), §5 |
| F-15 broad factory pattern | §3.6 layer 3: the guard's refusal stands (safe side) and names its text; per-path layer first |
| F-16 stash passes a re-dirtied tree | the decision text sentence (§3.4) and `state-exits.md` |
| OW-1 reminder in the chat | §3.8, B2 (`done_line`, `reminder_line`, driver exits, note), B3 (`s4`, `s9`, row); F14 |
| OW-2 the factory's own files | §3.7 `factory_origin` (I-9), B1 rows and edges; carrier fork F12, node B6 |
| Found here (not in the verdict) | F0-25: the skill road's packet never showed a finding's `fix` — the reason `answers` is a field both roads print; the "+N more … below" sentence is queued to B5 |
