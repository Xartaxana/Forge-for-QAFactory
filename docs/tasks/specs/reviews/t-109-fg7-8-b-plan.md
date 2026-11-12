# t-109 — critic on the PLAN: FG7-8 part B (B-13), `docs/tasks/specs/fg7-8-b-vcs-words.md`

Reviewer: critic (Opus). Date: 12.11.2026. Kind: plan gate (no code exists yet). B0's measurement
(`docs/tasks/specs/reports/t-110-b0-git-measure.md`, sent by the coordinator mid-review) is included.

**Verdict: GO WITH FIXES.** The plan holds up as a design: data rows, one reader, one executor, the
driver relay. The `shown_doors` and waiver mechanics close end to end on the driver road (key 2 a/b, traced
below). But B2 as written is not executable safely, for four reasons:
- its git command form fails on two common porcelain classes;
- its failure path destroys a staged split and merge-conflict state;
- its undo text is false on most classes;
- its waiver call is refused by `waiver.py`'s CLI.

There are also four spec-level contradictions: the skill road has no shown-state check, I-3 contradicts B3,
the packet's "How to answer" block does not list the new words, and "listed above" is false when there are
more than 5 paths. Ten blocking items (B-1 to B-10) must be fixed in the spec text before B1 or B2 is
dispatched. None needs a new architecture. B-8 is a fork for the Lead/owner. The Lead edits the spec; the
decision to accept the plan belongs to the Lead tier (critic rule 6).

---

## Blocking items

### B-1 — B2's git command form and class handling (§4 B2 steps 4-8, B0 "Both outcomes")
**Evidence (measured on git 2.56):**
- B0 report lines 615-655 and 709-748. `git add -- <paths>` exits 128 for a staged delete (`D `) and for a
  staged rename with both sides passed (`pathspec 'old9.txt' did not match any files`). So class 13 (a mixed
  tree) fails as a whole. My own probe reproduced it (scratch `g1`: `git add -- old.txt new.txt ...` exit 128).
- `git stash push -u -- <paths>` on the same classes exits 128 AND leaves a stash entry while the tree is
  unchanged (B0 lines 645-654, 739-748, 1063-1089). My probe `g4-s` reproduced it with `:(top,literal)`
  pathspecs too: exit 128, `stash@{0}: On master: QA` present.
- Quoted porcelain text passed as-is: commit gets 128; stash gets exit 0 `No local changes to save` (a
  silent no-op; B0 773-794, 872-893).
- A submodule pointer under stash: exit 0, silent no-op (B0 979-1000).
- NOT in B0, my probe `g3` (merge in progress, `UU c.txt`): `git add -- c.txt` exit 0 marks the conflict
  resolved with the conflict markers staged. Then `git commit -- ...` fails with `fatal: cannot do a partial
  commit during a merge`.

**Why it blocks:**
- Step 4 refuses only quoted paths and "classes B0 marked unsafe", so a staged delete or rename makes every
  `commit` fail.
- Step 8 treats a non-zero exit as "nothing was done", but stash 128 HAS made a stash entry.
- Step 7's success test is "exit 0 on every step", but stash exit 0 can mean nothing was done.
- Unmerged entries and in-progress merge/rebase/cherry-pick/revert states are not named at all (key 7).

**Proposed spec text (B2 steps 4-8):**
- **Read the paths losslessly** with `git status --porcelain=v1 -z` (unquoted paths, NUL-separated; a rename
  comes as `R  new\0old\0`). With that, classes 10 and 11 are taken instead of refused. My `g4` probe shows the
  `-z` form. The digest is computed from the same `-z` read. `check_vcs`'s message keeps its non-`-z` call
  byte-identical.
- **Refuse before any git write**, with the door "commit or stash it yourself, then answer `go on`", naming
  the path, when:
  - any entry is unmerged (XY in `DD AU UD UA DU AA UU`); or
  - `git rev-parse --git-path` names an existing `MERGE_HEAD`, `CHERRY_PICK_HEAD`, `REVERT_HEAD`,
    `rebase-merge` or `rebase-apply`; or
  - HEAD is detached (`branch == "HEAD"`), for commit (see F-8); or
  - for `stash` only: any entry has X = `D`, `R` or `C` (a staged delete, rename or copy), or is a submodule
    pointer (B0: a half-done stash or a silent no-op).
- **Commit form:**
  - `git add -- <paths of entries with a worktree change: Y != ' ' or '??'>`. This form leaves out the old
    side of a rename and staged-only deletes; skip the add when that list is empty.
  - Then `git commit -m MESSAGE -- <every path, both rename sides and staged deletes included>`. My probe
    `g4` (`D `, ` M`, `R `, `??` together): add exit 0, commit exit 0, `git show --name-status HEAD` =
    `D del7.txt / M m.txt / R100 old9.txt new9.txt / A u.txt`, tree clean.
  - B0 is re-run on this exact form (a B0b row per class) before B2 is accepted.
- **Success is the measured post-state, never the exit code:**
  - commit: HEAD moved, `HEAD^ == head_before`, `git diff --name-status head_before HEAD` covers exactly
    the listed paths, and `vcs_changes(...)["dirty"]` is empty.
  - stash: `git rev-parse -q --verify refs/stash` changed to a new sha whose subject carries MESSAGE, and
    `dirty` is empty.
  - Anything else is a problem that names the facts (see F-2).
- **A stash ref that changed while stash exited non-zero** is reported as a problem with the stash sha
  ("a stash entry was left: <sha>; your tree is unchanged"). It is never dropped automatically and is never
  recorded as a pass.

### B-2 — The undo text is false on most classes (§4 B2 step 7, §3 AR-25 row, B3 `state-exits.md`)
**Evidence:**
- B0 table, lines 1137-1148 and 1159-1166: after the commit, `git reset --soft HEAD~1` restores the "before"
  porcelain only for `M ` and `A `. Everything else comes back staged. `MM` loses its split: the person's
  staged version is gone from the index.
- My probe `g1`: after the reset, ` D` became `D `, `MM` became `M ` (index now `x3`, was `x2`), ` M` became
  `M `, and `??` became `A `.
- B0 lines 457-462 and 533-538: plain `git stash pop` loses the staged state. `pop --index` restores it
  (479-484, 555-560). My probe `g2` matches.

**Proposed text:**
- Before a commit, take `index_tree = git write-tree`. This is cheap, writes only an object, and is
  possible once B-1 has refused unmerged entries.
- The commit's undo is "`git reset --soft <head_before12>` then `git read-tree <index_tree12>`". It restores
  HEAD and the exact index; the worktree was never touched. Name it in the record and in `state-exits.md`.
- The stash's undo is "`git stash apply --index <stash sha12>`, then `git stash drop` of that entry". Name
  the stash by its sha, not `stash@{0}`, which moves when anything else stashes.
- Add a B2 test row: after the commit plus the named undo, porcelain equals the "before" porcelain for every
  class B2 takes (`MM` included). The same row for the stash.

### B-3 — The failure path's `git reset -q -- <paths>` destroys what the person had staged (§4 B2 step 8)
**Evidence:** my probe `g3`. After `git add -- c.txt w.txt` on `UU c.txt`, `git reset -q -- c.txt w.txt`
gave exit 0. Porcelain became ` M c.txt / ?? w.txt`, and `ls-files -s` shows a single stage-0 entry: the
conflict stages are gone, while `MERGE_HEAD` stays. The same mechanism on `MM`: when a hook refuses the
commit, the index is reset to HEAD, so the person's staged version (`x2` in `g1`) is lost. Step 8's claim
"so the index is as before" is false whenever an entry had a staged change.

**Proposed text:** on any failure after `git add`, restore with `git read-tree <index_tree>` (from B-2), not
`git reset -- <paths>`. Add a test row: `MM` plus a pre-commit hook that exits 1. After the failure,
porcelain is `MM`, and `git show :<path>` equals the staged content from before. B-1's refusal keeps
unmerged states from reaching this point at all.

### B-4 — Commit has no guard for the factory folder; the guard cannot serve as AR-15's survivor here (§1 I-2/I-4, AR-15 row, §4 B2 step 5 and test row)
**Evidence:**
- `stage_guard.py:2361-2396` (`rule_pathspec`) checks only `-a` and the presence of `--` or paths. It never
  refuses a `qa-factory` path. Only `rule_stash` (`:2433-2437`) does.
- `gate_preflight.py:244-258` (`outside_factory_home`) KEEPS a rename line when either side is outside the
  factory home. B2 step 4 then splits both sides, so `R  qa-factory/x -> src/y` puts `qa-factory/x` into
  `git add`/`git commit`.
- `rule_manifest` is `rule_manifest(ticket, what, event, *, required, pipeline, task_root)`
  (`stage_guard.py:1037`), not a command-text function. It is also vacuous at gate A: no manifest exists
  yet and `required` is false, so it returns None (`:1047-1053`).
- The rules cut the command tail at `;`, ` && `, `\n` and ` | ` before `shlex` (`stage_guard.py:2325-2328`,
  `2350-2353`). A path containing `;` therefore hides every later path from `rule_stash`.

So the B2 test row "a path list holding `qa-factory/x` is refused by the executor with the guard's text"
cannot pass for `commit`.

**Proposed text:**
- The executor's own first check is per PATH, not per line: every path (both rename sides) must lie outside
  `_factory_home_in_repo(...)`, else it refuses, naming the path.
- When the home cannot be told (`""`) while the factory home is inside `top`, it refuses.
- The guard rules are then asked as a second layer on `shlex.join(argv)`. State in the spec that they are
  advisory for commit (rule 5 holds the pathspec form, not the folder).
- `rule_manifest` is dropped from the executor, with one sentence why (no manifest before S5), or called
  with its real signature.
- Rewrite the AR-15 row accordingly: "the survivor of 'never the factory's folder' is
  `outside_factory_home`'s home, read per path; the guard is the survivor of the command FORM".

### B-5 — With more than 5 dirty paths, "listed above" is false and the write takes paths the person was not shown (§1 I-2, §3.1 `says`, B1 edge "More than 5 dirty paths")
**Evidence:** `gate_preflight.py:1944-1945` names the first 5 paths and then "and N more". The `says` of
`vcs_commit`/`vcs_stash` reads "the uncommitted changes listed above". I-2 reads "takes exactly what the
person was shown". The digest pins the set, but the person never saw entries 6 to N.

**Proposed text:** when `len(dirty) > 5` and a repository-writing door is offered, the `fix` lists every
path (or the first `K` with the rest in a details file the hint names). The `says` reads "all N uncommitted
changes (the list above names <shown>, the rest ...)". Alternatively: no commit/stash door above a stated
count, with that count a named limit and a B1 test at and beyond it. Choose one in the spec.

### B-6 — The packet's "How to answer" block omits the new words and says only its forms are read by code (FR-10, AR-16; §7 FR-10 claim; B1 owns)
**Evidence:**
- `gate_brief.py:2854-2876` (`_finding_forms`) offers only `<item id>: accept <your reason>` and
  `approve as is`.
- `gate_brief.py:1046-1047` (`ANYTHING_ELSE_SENTENCE`): "only the forms above are read by code".
- The rehearsal section (`driver_gates.py:120-124`, `render`) will print `vcs-test-repo: commit|stash|go on`,
  which code DOES read. The packet contradicts itself. §7's "accept and the three words are all read" is
  true of reading, false of the listing.
- `answer_forms` is "EVERY form of an answer this gate-A packet offers" (`:2895`).

**Proposed text:**
- B1 also owns `gate_brief._finding_forms`. For a line item whose `waives` holds an option with a
  `finding_door_words` row, it adds one form per offered word: `<item id>: <word>`, example `<real id>:
  <word>`, reader `Driver.read_finding_doors`, `where` "After your approval".
- B1's existing row in `test_answer_forms_are_one_list_and_each_has_its_reader` then proves each example is
  read.
- The same gap stands for `product_gap` today. Name it as a sibling (fixed by the same row, or queued).

### B-7 — B2 step 7's waiver call is refused by `waiver.py` (§6 item 3, settled)
**Evidence:**
- `person_words.py:144-148` raises `WordsRefused` when both the inline option and `--words-file` are given.
  `waiver.py:1631-1636` calls it with `--decision`/`--words-file`.
- So "`--words-file <words_ref>`" plus "the decision text is `person_decision(...)` + facts" cannot both
  reach the record.
- The driver's generic branch records with `--decision said` (`driver_machine.py:2864-2866`).

**Proposed text:** settle §6 item 3 in the spec as follows.
- The executor writes ONE words file through `person_words.write_words` (the one writer). It holds
  `person_decision(word, line, replaced)` plus `"; done: ...; to undo: ..."`, and the executor records with
  `--words-file` only.
- Or, on the driver road, keep `--decision` exactly as the generic branch does.
- Also name the record ROUTE: `repo_words.run` is a module function. Either it spawns `waiver.py` with the
  caller's environment (the driver's `self.py` carries the project env and `waiver_road()`), or it returns the
  facts and the caller records them through its existing waiver road (driver: `self.py("waiver.py", ...)`;
  CLI: its own subprocess).
- The second option keeps one writer and needs no new environment handling. State which.

### B-8 — The skill road has no shown-state check, so I-2 holds on one road only (P31, axis 34, AR-19; §4 B2 step 9, B3)
**Evidence:**
- On the driver road a line is read only when the stored `shown_doors` equal the fresh `waives`
  (`driver_machine.py:3150-3153`).
- The CLI (`repo_words.py --word ...`, step 9) "runs a fresh `gate_preflight` rehearsal of gate A and takes
  the finding's door for the word". It then passes that fresh block as `door_block` to `run`, whose digest
  check (step 3) compares fresh with fresh and always passes.
- The skill road therefore commits whatever is dirty at the moment the orchestrator runs it, not what the
  person was shown. The digest block is machine data that nothing prints (`gate_preflight.py:1321-1323`), so
  the orchestrator cannot copy it from the packet either.
- SIBLING_MAP axis 34 (`docs/SIBLING_MAP.md:589`): a road that leaves one side out "is a fork to the Lead
  and the owner, never a fact".

**Proposed fork (Lead; owner if it narrows a road):**
- (a) The skill-road gate stores what it showed (`shown_doors` per finding, the same shape as the driver
  road). The CLI takes `--shown <that record>` and refuses when it is absent or differs. One check, two
  roads.
- (b) The CLI takes the person's shown packet file (`--packet <file>`) and requires `[vcs-test-repo]
  <message>` in it, plus a digest the hint prints in words (weaker: the paths only).
- (c) The skill road offers only `go on` until (a) exists. This is an exclusion from a shared mechanism, so
  it needs a data row and the owner's word (rule 19, P31).

Recommendation: (a).

### B-9 — I-3 contradicts B3 (§1 I-3, §4 B3 behaviour and edges)
**Evidence:**
- I-3: "commit/stash run only from the closed word ... Free words ... go to the conductor".
- B3's conductor-actions row: "(or says so in other words that map to exactly one of them)" and then runs
  `repo_words.py`. B3 edges: "a word the orchestrator maps from other words is run only when the mapping is
  to exactly one word".
- B3's own `s4.md` sentence: "Nothing is committed or stashed on a word you inferred".
- On the driver road, an unread line (`commit please`) goes to the conductor, which by this row maps it and
  runs the CLI. So in practice a repository write DOES run on a role's reading of free words.

The spec states three incompatible rules for the same action.

**Proposed text:** one rule, in I-3, in `s4.md` and in the conductor-actions row alike. Recommended: "code
never infers; the conductor or orchestrator may map other words only when they name exactly one of the
words AND carry no condition or question. It runs the CLI with the person's line in `--words-file` and
`--by conductor|orchestrator`, so the record shows it was a mapping. In doubt it asks and never runs" (P27:
the reading is a role's judgment). Delete "nothing is committed on a word you inferred", or define "inferred"
as "not named in the person's words".

### B-10 — `repo_words.run` is a census unit, and B2 does not own the census fixture (§1.1, §6 item 2, settled; B2 owns)
**Evidence:**
- `scripts/tests/test_judgment_census.py:61`:
  `UNIT_NAME_RE = ...|^_?(check|run)$|...`. A function named `run` is a unit by name (u1), whatever it
  raises.
- B2's owns has no `scripts/tests/fixtures/judgment-census.json`. B2's DoD runs `test_judgment_census.py`,
  which then goes red.

**Proposed text:**
- B2 owns `judgment-census.json` (one row: `repo_words.run`, class `safety`, owner `intent`). The
  `safety` ceiling 54 → 55 is named in the verdict (AR-20).
- Or rename the function so it is not a unit, which is legitimate only if it holds no check. It does hold
  the B-1/B-4 refusals, so take the row.
- `finding_door_option` and `finding_door_hint` do not match the regex: no row.

---

## Non-blocking items

- **F-1 — The digest pins entries, not content (§5 small choices "Digest").** An untracked folder `?? dir/`
  stays one line while new files appear in it, and `git add -- dir/` takes them (B0 class 2 shows the folder
  expanding). Proposal: compute the digest from `--porcelain=v1 -z -uall` (per file). Optionally include
  `git hash-object` of each listed file, so a later edit unreads the line too. State that the person's own
  edits between show and answer are taken otherwise.
- **F-2 — Success with a dirty tree remaining.** A hook such as lint-staged or a formatter can change files,
  so the commit exits 0 and the tree stays dirty. The waiver on `head_after` would then silently pass the new
  dirty finding (GW1-43 semantics). Under B-1's post-state check this becomes a problem that names the
  remaining paths: "the commit IS made ...; these are still uncommitted: ...". The waiver is still recorded,
  since the person said `commit`, but the conductor is told.
- **F-3 — Timeout (step 8).** A killed `git commit` can leave `.git/index.lock`, which blocks the person's
  git afterwards. On Windows, `subprocess.run(timeout=)` kills git but not the hook's children. The problem
  text should check for and name a leftover `index.lock`, with the door "if no git is running, delete it".
- **F-4 — `closed_by_run` closes nothing on an unreadable pipeline** (`external_writes.py:196-202`). For a
  write into the person's repository the safe default is the reverse: the executor refuses when
  `pipeline.json` cannot be read (AR-28 for a write). The edge "closed_by_run raises" never fires, because the
  function does not raise.
- **F-5 — `accept <reason>` and `go on` pass the same block with one action**, one requiring a reason and
  one not. Say in the hint why both stand (accept is the universal door, FR-4), or make the vcs finding's
  `go on` the only word and keep `accept` for the line door. The Lead's call. This is not a P31 road split,
  but it is two words for one effect.
- **F-6 — The undo text reaches the person through `waiver.py --list`** ("Blocks passed by your word so far",
  `driver_gates.py:128-130`) and carries git commands with flags. Run it through `human_text.problems(...,
  kind="report")` in a B2 row, or put the git command in backticks as the person's own tool, per
  `human-questions.md`'s rule on commands.
- **F-7 — `--stage S5` is a literal in step 7.** Use the door's own `stage` (`door()` stores
  `self.next_stage`), as the generic branch does (`driver_machine.py:2865`).
- **F-8 — Detached HEAD.** `branch == "HEAD"` makes "on this branch" false, and a commit there is easy to
  lose. Refuse commit (B-1) or name it in `says`.
- **F-9 — Stash against `test_repo_base`/`test_novelty`** (§6 item 8 covers commit only). A test file that
  was dirty at S0 and is stashed afterwards no longer matches its recorded S0 hash
  (`test_novelty.py:268-279`, `544-559`), so it may read `dirty_changed`/lost. Not run; by reading only. Add
  it to §6 or to a B2 row.
- **F-10 — Adversarial battery additions** (B1 test table):
  - a Cyrillic homoglyph `сommit` (U+0441), built from code points;
  - a full-width `ｃｏｍｍｉｔ`;
  - `go on` (NBSP: `str.split` folds it, so it IS read; state that as the intended result);
  - a bulleted and a backticked id (`- \`vcs-test-repo\`: commit`);
  - two lines `commit` then `commit?` (the last is unread, so the earlier one is set aside,
    `driver_machine.py:3181-3184`).
  - The 1001-character row tests no limit (`finding_door_option` has none). Keep it as magnitude, labelled
    as such.
- **F-11 — Test placement (TESTING.md layers).** `test_words_doors.py` is the sole AR-24 detector
  (F0-19). Only the CLI's `--words-file` / `door()` row belongs there. The git-behaviour table (commit,
  stash, hook, stale, no-trace, factory path, undo) belongs in a keep file of the gate. §6 already names
  `test_gate_question_form.py`, which builds a `Driver.__new__`, as the fallback. Make it the plan, not the
  fallback. Both are keep files; no quarantined file is touched.
- **F-12 — Duplication and consistency in `_record_door_lines`.** Today it dispatches on
  `door.get("option") == "product_gap"` (`driver_machine.py:2847`). B2 adds a dispatch on the row's
  `executor`. Two dispatch styles would live in one loop. Since `product_gap` gains `"executor":
  "product_gap"` (§3.1), dispatch every branch on `executor`, and keep the generic waiver as the `record`
  executor.
- **F-13 — Packet length.** Three words × (1 + 3 price lines) adds 12 or more lines under the vcs finding in
  the rehearsal section. Confirm no line cap of the gate text cuts it. `brief_lines` does not print the
  `fix` of a non-story-level row (`gate_preflight.py:5983-5985`), so only `render` carries it.
- **F-14 — F1's "product code included".** Committing the person's product work-in-progress onto their
  branch with a factory message is a product and process risk, which PROJECT.md says to put to the owner.
  The Lead marked it "until the owner's word". Keep it marked, and add it to the owner's question list
  beside F3.
- **F-15 — A broad factory pattern.** `_names_factory` (`stage_guard.py:2399-2401`) matches any path ending
  in `qa-factory`, so a legitimate product path can make `rule_stash` refuse. With B-4's per-path check
  primary, a refusal from the advisory layer must name the guard text (already planned).
- **F-16 — State in the record** that after `stash` the HEAD-block waiver also passes a tree made dirty again
  at the same HEAD (GW1-43), for example after the person pops early. One sentence in the decision text or
  in `state-exits.md`.

---

## Key 1 — FACTS by trail

| Fact | Checked at | Result |
|---|---|---|
| F0-5 | `gate_preflight.py:1318-1326` (door, 60-char cut, `"`→`'`), `:1338-1353` (waiver_command), `:1394-1414` (add → `split_overridden(matched_text(...))`) | correct |
| F0-7 | `gate_brief.py:776`, `:779-793`, `:796-809`, `:812-814`, `:709-714` | correct |
| F0-10 | `driver_machine.py:3078-3185`. Read order: stand-gap whole, then canonical first word, then `finding_door_option` (`:3136-3144`). `fit` at `:3163`. Last line wins (`:3173-3184`) | correct |
| F0-11 | `driver_machine.py:2769-2801`, `:2837-2877`, product_gap `:2847-2863`, generic `:2864-2876` (uses `--decision`), failed → note/hold `:2613-2626` | correct |
| F0-14 | `stage_guard.py:2361`, `:2410`, `check_command :2845-2877`, rule 3 applied at `:2870` | correct as a citation. But `rule_manifest` is not a command-text function (`:1037`), see B-4 |
| F0-15 | `external_writes.py:189-202`; `conductor-actions.json:26-29` | correct. Note F-4 (unreadable means open) |
| F0-1/2/3/4/6 (spot) | `gate_preflight.py:1917-1953`, `:210-220`, `:237-258`, `:5811-5814`, `:5980-5985` | correct |
| F0-9 | `question-vocabulary.json:91-101` | correct. No stand-gap or approval word collides with `commit`/`stash`/`go on` (`gate-approval-words.json` read whole) |
| F0-16 | `conductor-actions.json:30` | correct |

### §6 items settled
- Item 1 (git per class): settled by B0 plus my probes `g1` to `g4`. Results are in B-1 to B-3.
- Item 2 (census): settled. `run` is a unit by name (`test_judgment_census.py:61`), so it needs a row
  (B-10). `finding_door_option` is not a unit.
- Item 3 (`--words-file` plus composed decision): settled, it is refused (`person_words.py:144-148`). See
  B-7.
- Item 4 (signatures): settled. `contract.person_decision(word, line, replaced=()) -> str`
  (`contract.py:579-583`). `Driver.words_file(words, name)` returns a path or None
  (`driver_runner.py:321`).
- Item 5 (harness): partly settled. `test_words_doors.py` imports `test_gate_preflight` (`:44`), which
  holds `check_vcs` fixtures. Placement is F-11.
- Items 6-8: not settled, beyond F-9's reading on item 8.

## Key 2 — FEASIBILITY

- **(a) The 60-char cut and `shown_doors == waives`.** `test repository changes: ` is 25 characters, plus
  12 + 1 + 12 = 50 ≤ 60, so the block survives `door()` (`:1325`). The comparison is a `json.dumps(sort_keys)`
  of the whole `waives` list (`driver_machine.py:3150-3151`). Both the show-time and the answer-time
  rehearsal register the same 4 doors in the same order, so equality holds when HEAD, the set and
  `closed_by_run` are unchanged. A change in any of them unreads the line, which is the intended direction.
- **(b) The waiver drops the finding at the next rehearsal.** `add` matches each live override's `match`
  with `contract.names_whole` against `matched_text(message, doors)` = the message plus every door block
  (`gate_preflight.py:129-132`, `waiver.py:202-222`, `contract.py:132-152`). The stage is `self.next_stage`,
  which is S5 at gate A.
  - **go on:** the waiver is on the HEAD block, which is in the dirty finding's accept and go_on doors, so
    it is dropped (as today).
  - **commit:** the waiver is on `test repository state: <head_after12>`. The next rehearsal's clean-branch
    finding carries that block in its accept door, so it is dropped. The needle's right edge is followed by a
    space or the end of the text, so `names_whole` holds.
  - **stash:** HEAD is unchanged, so the HEAD block of the clean finding is dropped.
  - **Caveats:** (b) holds only if the record is actually written (B-7), and for commit only if the tree is
    clean afterwards (F-2).
  - `waiver.py`'s `block_standing` holds the block against the standing-refusal record. At gate A that
    record normally holds nothing for S5, so the record is made with "not verified", the same as today's
    HEAD door.
- **(c) `stage_guard.rule_*` from a script.** `rule_pathspec(command)` and `rule_stash(command)` take a
  string and need no context. They are callable on `shlex.join(argv)` (they `shlex.split` the tail). They are
  lossy on a path containing `;` or `&&`, and `rule_pathspec` never checks the factory folder.
  `rule_manifest` needs `ticket`/`task_root` and is vacuous before S5. See B-4.
- **(d) Delete and rename entries.** `git add -- <paths>` is wrong for `D ` and `R ` (exit 128, measured).
  `git commit -- <old> <new> <deleted>` after an add of worktree-changed entries only works (my probe `g4`).
  See B-1.

**The end-to-end road** is: shown packet → line → `read_finding_doors` → `_record_door_lines` → `run` →
waiver → next rehearsal.
- Driver road: closes after B-1, B-3, B-4 and B-7.
- Skill road: does not hold I-2 (B-8).

## Key 3 — SAFETY

| Road / case | Status |
|---|---|
| Inferred word | Code: no. F5-a, plus `?` unread (`:3154-3155`), plus the last line wins. Role: yes by B3's row. The contradiction is B-9 |
| Stale change set | Driver road: guarded by the digest (entries, not content, F-1). Skill road: unguarded (B-8) |
| No-trace run | Guarded twice (hint and executor). Unreadable pipeline: F-4 |
| Takes `qa-factory/` | Commit is unguarded for a rename line (B-4). Stash is guarded by rule 7 |
| Takes what was not shown | More than 5 paths (B-5); new files in a shown untracked folder (F-1) |
| Partially staged tree (`MM`) | The commit takes the worktree content (B0 lines 510-511). The person's split is lost on success and on failure (B-3). The undo text does not restore it (B-2) |
| Undo: `git reset --soft <before>` | True only for `M ` and `A ` (B0 table) |
| Undo: `git stash pop` | Loses staging. `--index` keeps it (B-2) |

## Key 4 — ARCHITECTURE and principles

**AR rows:**
- AR-1: kept (rows plus a capability key). The DoD grep is sound: today `gate_preflight.py` and
  `gate_brief.py` have no `"commit"`/`"stash"`/`"go on"` literal (Grep -i). `driver_machine.py` has
  `"go on"` tokens of other questions, which is outside B's grep scope.
- AR-9: kept once B-1's refusals carry doors.
- AR-13: kept (`vcs_changes`, `vcs_state_block`). The `-z` read of B-1 must live in `vcs_changes`, not in
  the executor.
- AR-14: kept, with a choice of record route (B-7).
- AR-15: NOT kept as claimed (B-4).
- AR-16: NOT kept until B-6 is fixed.
- AR-17: kept (existing relay, no new stop).
- AR-19: B-8.
- AR-22: kept, if `finding_door_words` returns the new keys and `_relay_note` reads the word.
- AR-24: kept (the line is quoted whole, B-7 aside).
- AR-25: kept once the undo is true (B-2).
- AR-28: kept, plus F-4.
- AR-29: kept. Every check is data or safety, and the role's mapping stays a role's (B-9).

**FR and P rows:**
- FR-7: kept (key 2b), with F-2.
- FR-9: kept on the driver road.
- FR-12: kept on the code side.
- FR-36: kept.
- FR-53/P8: kept with F2-a.
- FR-57: kept: no `--no-verify`, no `-c` (B0's script used `-c user.*`, but only in the measurement).
- P13: the person's word passes the gate, and a failure goes to the conductor.
- P22: kept (failures go to the conductor once).
- P27: kept, if B-9 is resolved toward "the role maps, code reads exactly".
- P31: B-8.

Code judging what a role or the person should judge: none found. The class refusals are git-state facts
(data/safety), not meaning.

**DUPLICATION AND CONSISTENCY (rule 18):** F-12 (two dispatch styles in `_record_door_lines`). The twin
note `_record_gap_lines`/`_record_door_lines` (`driver_machine.py:2808`, `2842`) is unchanged by the plan.
Grepped: `"commit"|"stash"|"go on"` -i in `gate_preflight.py`/`gate_brief.py`/`driver_machine.py`.

**CODE QUALITY (rule 18):** at plan level, the B2 step list conflates "exit 0" with "done" (B-1) and names a
guard function with the wrong signature (B-4). No other finding.

**ONE ACTION, ONE ROAD (rule 19):** B-8 blocks. The skill road lacks the shown-state check the driver road
has. No owner word or data row covers the difference. Proposed node: the fork in B-8, owner the Lead
(owner's word if (c)).

## Key 5 — The Lead's fork decisions

- F1 (a): sound, with F-14 (an owner item) and B-5 (the "shown" set must really be shown).
- F2 (a): correct, since P8 is direct.
- F3 (a): sound once B-7 fixes the record form. The owner question on "Left with you" is correctly routed.
- F4 (a): fine, with B-6 (the forms list) and F-13.
- F5 (a): safe. It is the right direction for a write.
- F6 (a): correct. Add `product_gap`'s missing answer form (B-6) to B5 or fix it in B1.
- F7 (a): fine, but it must exclude the classes B0 showed fail or no-op (staged `D`/`R`/`C`, submodule;
  B-1).

None is unsafe as a decision. B-8 is a new fork the plan did not list. It belongs to the Lead, and to the
owner if option (c) narrows a road.

## Key 6 — NODES

- **Executability by a weaker model:**
  - B1 is close. It must add `_finding_forms` to owns and behaviour (B-6) and the >5-paths text (B-5).
  - B2 is not executable as written: B-1, B-2, B-3, B-4, B-7 and B-10 each change its steps or owns.
  - B3 needs B-9's single rule and, if B-8 (a), the skill-road store of shown doors.
- **Owns overlap:**
  - B1, B2 and B3 are disjoint from each other.
  - B1 against part A: disjoint functions in `gate_preflight.py`/`gate_brief.py`, as §4.0 says, with
    `очередь: A → B` (PROJECT.md «Командная работа» item 3). `_finding_forms` (B-6) is not part A's either.
  - Missing from owns: `judgment-census.json` for B2 (B-10). `driver-layers.json` stays conditional.
- **Test layers:** rows in keep files only (`test_gate_vocabulary.py`, `test_gate_question_form.py`,
  `test_words_doors.py`). No quarantined file is edited (`test_decision_classes.py` and
  `test_d1_product_gap.py` are untouched). Placement: F-11.
- **Adversarial battery:** sufficient on magnitude, case, separator and question. Additions are in F-10.
  B-1's class-refusal table and B-2's undo rows are new rows B2 owes.

## Key 7 — Missing edges

- Unmerged entries; merge, rebase, cherry-pick or revert in progress (B-1).
- Detached HEAD (F-8).
- Stash exit 128 that leaves an entry, and stash exit 0 that does nothing (B-1).
- A staged delete or rename for stash (B-1).
- Hook-modified tree after a successful commit (F-2).
- `index.lock` after a timeout (F-3).
- Unreadable `pipeline.json` (F-4).
- More than 5 paths (B-5).
- New files inside a shown untracked folder (F-1).
- The record route's environment (B-7).
- The skill road's shown state (B-8).
- Stash against `test_novelty` (F-9).

## What B2 must become, given B0 (the coordinator's question)

1. **Command form:** read with `--porcelain=v1 -z` in `vcs_changes`. Commit = `git add --
   <entries with Y != ' ' or ??>` (skipped when empty), then `git commit -m MSG -- <all paths, both rename
   sides, staged deletes>`. Stash = `git stash push --include-untracked -m MSG -- <paths>`, only for classes
   B0 shows exact. B0b re-measures this form per class.
2. **Class refusals before any write:**
   - both commit and stash: unmerged XY; MERGE/CHERRY_PICK/REVERT/rebase in progress; a path inside the
     factory home (per path, both rename sides);
   - commit only: detached HEAD;
   - stash only: X in `D R C` and a submodule pointer.

   Quoted classes are no longer refused, once the `-z` read is used.
3. **Success test:** the post-state, never the exit code:
   - commit: HEAD moved with parent `head_before`, `diff --name-status` equals the list, `dirty == []`;
   - stash: a new `refs/stash` sha with MSG, `dirty == []`;
   - a stash ref that changed on a non-zero exit is a named problem, never dropped and never a pass.
4. **Failure restore:** `git read-tree <index_tree>` from a `git write-tree` taken before the add, never
   `git reset -- <paths>`.
5. **Undo text:**
   - commit: `git reset --soft <head_before12>` then `git read-tree <index_tree12>`;
   - stash: `git stash apply --index <stash sha12>` then drop that entry.

   A test row proves that porcelain after the undo equals the "before" porcelain, per class.

---

## Trail

**Read:**
- `docs/tasks/specs/fg7-8-b-vcs-words.md` (whole)
- `docs/tasks/specs/reports/t-110-b0-git-measure.md` (whole)
- `scripts/gate_preflight.py`: 120-144, 200-264, 1300-1444, 1880-1990, 5787-5821, 5917-5992
- `scripts/gate_brief.py`: 420-569, 700-820, 1046-1049, 2840-3069
- `scripts/driver_machine.py`: 2490-2980, 3060-3230
- `scripts/driver_gates.py`: 90-140
- `scripts/waiver.py`: 1-956, 1440-1659
- `scripts/person_words.py`: Grep `def read|def door|both` with context
- `scripts/stage_guard.py`: 1030-1090, 2280-2440, 2840-2890
- `scripts/external_writes.py`: 185-204
- `scripts/contract.py`: 132-157, 579-584
- `scripts/test_novelty.py`: Grep `head|dirty`
- `scripts/tests/test_gate_question_form.py`: 735-840
- `scripts/tests/test_judgment_census.py`: Grep
- `scripts/tests/test_words_doors.py`: Grep of its heads
- `references/question-vocabulary.json` (whole)
- `references/gate-approval-words.json` (whole)
- `references/conductor-actions.json`: 20-33
- `docs/SIBLING_MAP.md`: Grep axis 34 / row 139
- `tools/critic_verdict.schema.json`

**Greps** (positive controls: each search had hits in the same call or a sibling call):
- `test repository` -i over the package (hits)
- `"commit"|"stash"|"go on"` -i in the three scripts (hits in `driver_machine` only)
- `\["says"\]...` in `gate_brief.py` (empty; re-run as `open_rehearsal_items\(|...` with hits)
- `def person_decision|def words_file` (hits)

**Probes** (scratchpad, git 2.56.0.windows.2):
- `g1`: rename/MM/delete/space/untracked. Add exit 128 on the rename's old side. The corrected add and the
  commit succeeded. After `reset --soft`: porcelain `D /M /R /M /A`, index mm `x3` (was `x2`).
- `g2`: stash with MM plus qa-factory. Plain pop gives ` M mm.txt`, index `x`; qa-factory untouched.
- `g3`: `UU` merge. Add exit 0 stages the markers. Commit exit 128 "cannot do a partial commit during a
  merge". `reset -- paths` leaves a single stage-0 entry and gives ` M c.txt`; `MERGE_HEAD` present.
- `g4`: the add-worktree-only form plus commit of all paths: exit 0, name-status `D/M/R100/A`, tree clean.
- `g4-s`: stash of staged D+R with literal pathspecs: exit 128 and `stash@{0}` left.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B-1 B2 command form: git add -- paths exits 128 for staged delete and rename (B0 615-655, 709-748); stash exit 128 leaves an entry, stash exit 0 can be a no-op; unmerged/merge-in-progress not refused (probe g3); success must be the measured post-state, not exit 0",
    "B-2 undo text false: reset --soft restores only M and A classes (B0 table 1137-1166); plain stash pop loses staging; use write-tree/read-tree and stash apply --index <sha>",
    "B-3 failure path git reset -- paths destroys a staged MM split and merge-conflict stages (probe g3); restore with read-tree of a pre-add write-tree",
    "B-4 commit has no factory-folder guard: rule_pathspec (stage_guard.py:2361-2396) never checks qa-factory, outside_factory_home keeps a rename line (gate_preflight.py:244-258); rule_manifest is not a command-text function (stage_guard.py:1037); executor must check per path",
    "B-5 more than 5 dirty paths: message names 5 (gate_preflight.py:1944-1945) while says reads listed above; the write takes unshown paths",
    "B-6 FR-10/AR-16: _finding_forms (gate_brief.py:2854-2876) lists only accept, and ANYTHING_ELSE_SENTENCE (gate_brief.py:1046-1047) says only listed forms are read by code; B1 must own _finding_forms and add the word forms",
    "B-7 waiver call infeasible: --words-file with a composed decision is refused (person_words.py:144-148, waiver.py:1631-1636); name one form and the record route",
    "B-8 skill road compares a fresh door with a fresh door, so I-2 holds on the driver road only (driver_machine.py:3150-3153 vs B2 step 9); P31/axis 34 fork to Lead/owner",
    "B-9 I-3 says never inferred while B3 conductor-actions row runs commit on mapped other words and s4.md says nothing on an inferred word; one rule needed",
    "B-10 repo_words.run matches UNIT_NAME_RE (test_judgment_census.py:61); B2 must own judgment-census.json and name the safety ceiling raise"
  ],
  "fixes": [
    "Rewrite B2 steps 4-8 per the section What B2 must become: -z read in vcs_changes, add only worktree-changed entries then commit all paths, class refusals (unmerged, in-progress ops, detached HEAD for commit, staged D/R/C and submodule for stash), post-state success test, read-tree restore, true undo texts; add B0b rows for the new form",
    "Add a per-path factory-home check in the executor; restate the AR-15 row; fix or drop the rule_manifest call",
    "B1: own gate_brief._finding_forms and add one form per offered finding-door word; settle the more-than-5-paths text or limit",
    "Settle section 6 item 3 in the spec (one words file via person_words.write_words, or --decision as the generic branch) and name the record route",
    "Decide the B-8 fork (recommended: the skill-road gate stores shown_doors and the CLI requires it) and write one I-3 rule shared by s4.md and the conductor-actions row",
    "Add judgment-census.json to B2 owns with the repo_words.run row",
    "Fold F-1..F-16 where the Lead agrees (digest -uall, hook-dirtied tree, index.lock, unreadable pipeline, door stage, detached HEAD, battery additions, test placement, executor dispatch)"
  ],
  "class_completeness": "Surface: the gate-A finding-door word road (reader, packet forms, executor, record). Siblings walked: product_gap shares the missing answer form (B-6, fix in B1 or queue in B5); the clean-tree literal and check_stand literal are queued as B5 (F6); the skill-road twin is axis 34 and AR-19 (B-8); SIBLING_MAP axis 5 row to be added by B4. No sibling found outside the map beyond these.",
  "trail": {
    "read": [
      "docs/tasks/specs/fg7-8-b-vcs-words.md",
      "docs/tasks/specs/reports/t-110-b0-git-measure.md",
      "ai-packages/qa-factory/scripts/gate_preflight.py",
      "ai-packages/qa-factory/scripts/gate_brief.py",
      "ai-packages/qa-factory/scripts/driver_machine.py",
      "ai-packages/qa-factory/scripts/driver_gates.py",
      "ai-packages/qa-factory/scripts/waiver.py",
      "ai-packages/qa-factory/scripts/person_words.py",
      "ai-packages/qa-factory/scripts/stage_guard.py",
      "ai-packages/qa-factory/scripts/external_writes.py",
      "ai-packages/qa-factory/scripts/contract.py",
      "ai-packages/qa-factory/scripts/test_novelty.py",
      "ai-packages/qa-factory/scripts/tests/test_gate_question_form.py",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py",
      "ai-packages/qa-factory/scripts/tests/test_words_doors.py",
      "ai-packages/qa-factory/references/question-vocabulary.json",
      "ai-packages/qa-factory/references/gate-approval-words.json",
      "ai-packages/qa-factory/references/conductor-actions.json",
      "docs/SIBLING_MAP.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "scratch g1: git add -- old.txt new.txt mm.txt del.txt 'sp ace.txt' ud/ on a staged rename", "result": "fatal: pathspec 'old.txt' did not match any files, exit=128 (agrees with B0 class 9)"},
      {"command": "scratch g1: corrected add, commit -- all paths, reset --soft base", "result": "commit exit 0; after reset porcelain D del, M mm, R old->new, M sp ace, A ud/f; index mm x3 (was x2)"},
      {"command": "scratch g2: stash push -u -m QA -- mm.txt new.txt then plain stash pop", "result": "pop exit 0; porcelain ' M mm.txt'; index mm 'x' (staged x2 lost); qa-factory untouched (agrees with B0 class 5)"},
      {"command": "scratch g3: UU merge, add -- c.txt w.txt, commit -- c.txt w.txt, reset -q -- c.txt w.txt", "result": "add exit 0 stages markers; commit exit 128 cannot do a partial commit during a merge; reset leaves one stage-0 entry, ' M c.txt', MERGE_HEAD present"},
      {"command": "scratch g4: add -- m.txt u.txt then commit -- del7.txt old9.txt new9.txt m.txt u.txt", "result": "both exit 0; name-status D del7, M m, R100 old9 new9, A u; tree clean"},
      {"command": "scratch g4-s: stash push -u -m QA -- literal pathspecs of staged delete and rename", "result": "exit 128 and stash@{0} On master: QA left, tree unchanged (agrees with B0)"}
    ]
  }
}
```
