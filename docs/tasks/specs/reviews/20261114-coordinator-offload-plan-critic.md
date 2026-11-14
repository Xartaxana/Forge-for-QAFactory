# Critic on the plan: coordinator offload (t-844, plan t-842)

Plan under review: `docs/tasks/specs/20261114-coordinator-offload-spec.md` (untracked in the main checkout, 791 lines, read whole).
Checked against the root checkout at `50f4ed95` (= `origin/main`; the `read-main` worktree is stale at `e4df9c0f`, so I did not use it).
One pass. I propose the verdict below. Accepting it is the Lead's decision: final acceptance is queued to Fable (§11 of the plan).

## Verdict

**GO WITH FIXES.** The design holds up overall. The owner's asks are all present (key 6). The streams are cut along real seams.
The plan reuses the right readers in most places: hop_metrics' regex, the manifest cut, the hygiene decider, the manifest checker.
Six blockers have to be fixed in the spec before the streams they name are dispatched. Four of them come from runs or experiments, not from reading.
Each blocker is local and has a short fix. A3, A2 and C2 can go out now, apart from S-6 for A1 and S-8 for A2 under F-T1 (a).

## Blockers (fix in the spec before dispatching the named stream)

**BL-1 (B0/B1): rule 9a' refuses ids that `next` reserved. The cause is ids landing out of order, so two sessions on one file break routinely.**
§3.B0 item 2 makes a brand-new id legal only when "its number is GREATER than every number already seen WITH THE SAME LETTER". E-B0-4 depends on that ordering to refuse duplicates.
§3.B1 then hands out ids AHEAD of their lines: `next [--n K]` reserves 1..20 ids, and the dispatch carries `Task t-NNN` long before the hook writes the line.
Scenario, one machine, row 1 of the B5 table: session A runs `next` and gets t-900, then spends a minute composing its dispatch. Session B launches a dispatch with no task id; the hook issues t-901 and writes it.
A then launches. Its hook writes `delegated t-900`. 900 is not greater than the max 901, so 9a' refuses and the hook prints `NOT written`.
The same thing happens in ONE session: `next --n 3` gives t-900..t-902, and the dispatch for t-902 is sent first. It also happens for the pre-issued `Task t-NNN` of every dispatch whenever a hook-issued id lands in between.
This defeats the owner's word 2 (parallel sessions) in the first hour.
Fix: change 9a' to "a brand-new id was NEVER SEEN before (full id, letter included) in the logical journal, AND its number is at most `ID_JUMP_MAX` above the max of its letter".
E-B0-4 still holds through "never seen": a re-issued id is a seen id. E-B0-3 still holds through the jump cap. Add a row: "a reserved lower id written after a higher one is legal".
The writer can also check "reserved by this clone's counter" at write time. The validator cannot see the counter: it is local, and CI does not have it.

**BL-2 (B1): `accept --run` runs inside the journal lock as written, so the parallel session's hooks and CLI starve.**
"Common behaviour" fixes the order: take the lock → read → stamp ts → **build the object** → validate → append. The witness from `--run` (E-B1-8: up to 600 s) is part of building the object.
Read literally, the subprocess runs while the `journal` lock is held. During a 5-minute pytest, every hook call of every session times out at 5 s (E-B23-6: `delegated NOT written`). Every CLI call times out at 15 s (exit 3).
Fix: state the POSITIONAL invariant. `--run` and `--witness-file` are executed and read BEFORE the lock. The lock covers only read → validate → append → counter, and holding it is bounded to milliseconds.
Add a row: "a 30 s `--run` in session A, while session B's hook writes `delegated` during it → written".

**BL-3 (B1, E-B1-9): `--run` with `shell=True` on Windows runs cmd.exe, but the hygiene gate judges Bash syntax. That is a verified road around the gate.**
E-B1-8 prescribes `subprocess.run(<cmd>, shell=True, ...)`. On win32 that is `cmd.exe /c`. E-B1-9 judges the same text through `hygiene_gate._decide_command(..., tool="Bash")`, and its quoting rules are POSIX.
Both runs are verbatim in the Trail:
- the gate ALLOWS `echo ' >> logs\journal\dev1.jsonl '` with `(0, None)`, because in Bash the redirect sits inside single quotes;
- `subprocess.run(r"echo ' >> logs\journal\probe.jsonl '", shell=True)` in the scratchpad WROTE `logs/journal/probe.jsonl` with the content `"'  '\n"`.
The plan's invariant ("`--run` is not a road around the hygiene gate") is false on the target OS.
Fix: run exactly the shell that was judged, i.e. `[bash, "-c", cmd]` with bash resolved via `shutil.which` (Git Bash here; CI is Linux). When bash is absent, refuse.
Alternative fix: `shell=False` over `shlex.split(cmd)` with every shell metacharacter (`|&;<>$\`` and quotes left unbalanced) refused.
Add the cmd.exe single-quote row above to the E-B1-9 adversarial list.

**BL-4 (C3): after the first wave, step 9 ("refresh the root") can never succeed, and step 8 `git branch -d` runs before the root is refreshed.**
Step 10 commits the root's journal to origin on every wave. On the next wave, origin's journal differs from the root's HEAD, and the root holds uncommitted journal lines. That is exactly what the step-9 precondition allows.
`git merge --ff-only` then refuses. I ran the experiment in the scratchpad (Trail, verbatim): `error: Your local changes to the following files would be overwritten by merge: j.jsonl ... rc=1`, even though origin's content is a byte-prefix of the local file.
So the plan's own test row "journal prefix → refreshed" cannot pass without the builder inventing a mechanism, which PROJECT.md «Командная работа» п. 11 calls a defect of the dispatcher.
Step 8 has the same problem: `git branch -d` checks against the root's HEAD when no upstream is set. That HEAD is stale until step 9, so `-d` refuses "not fully merged" on every wave.
Fix: (a) Step 9 runs under the `journal` lock. Take a byte copy of the root's journal. Write the root's HEAD version of the journal over it (a byte copy, legal per hygiene pt.7). Run `merge --ff-only`. Restore the full bytes from the copy, then verify with a hash. Origin's version is a prefix of the copy, so the restored file = origin + the local tail.
(b) Delete the branch after step 9. When the root was not refreshed, delete it via `git merge-base --is-ancestor <branch> origin/main` followed by `git update-ref -d refs/heads/<branch>`, never `-D`.
(c) Add test rows: "two waves in a row: root refreshed both times" and "hook appends during step 9 (lock held) → no line lost".

**BL-5 (B23, E-B23-10): `returned` is lost when the delegating session lives in a second worktree (row 2 of the B5 table), and the loss is silent.**
`record_returned` looks in "the stop payload's cwd" journal, then in the first entry of `git worktree list`, and otherwise leaves a marker.
For a background launch, PostToolUse has ALREADY written `delegated` into the delegating session's worktree copy before the stop. Nothing ever consumes the marker, and it is pruned after 24 h (item 3) with no output.
Separately, the premise "the stop payload's cwd is the worker's worktree" is unmeasured. It also contradicts dod_gate's own model: the track lives at `<payload cwd>/.claude/dod_track/<session_id>.json`, and the session_id is shared by the main thread and its subagents (dod_gate.py:36-47, 580-585).
Fix: (a) Step 0 also measures the `cwd` of a SubagentStop for a worktree-isolated worker. (b) `record_returned` looks for `worker_ref == "agent:<id>"` in EVERY journal copy listed by `git worktree list --porcelain`, which is bounded.
(c) Pruning a marker prints one WARN line, read by check 48(c), instead of happening silently. (d) Add a test row: "delegating session in a linked worktree, background launch → `returned` written in that worktree's copy".

**BL-6 (A1, B0, B23 and the later prefix additions): builder commits to those paths are refused by the tier gate. "Only stream L needs Fable" is wrong.**
§2 says L alone lands through Fable "because CLAUDE.md, the calibration protocol and DECISIONS.md are mechanism paths".
In fact `tools/mechanism_gate.py:211-275` `MECHANISM_PREFIXES` also names:
- A1's `.claude/agents/`;
- B0's `journal_validator.py`, `journal_keys.py`, `session_context.py`, `journal_echo.py`, `compact_snapshot.py`, `forge_metrics.py`, `piles.py`, `dispatch_manifest.py`;
- B23's `dod_gate.py`, `hygiene_gate.py`, `mechanism_gate.py`;
- C2's `ci_read.py` and `ci_read_common.py`.
For a mechanism commit from a tier below the lead binding, `_tier_queue_note()` (:855-859) says the session "does NOT commit the mechanism itself -- it goes into the Lead queue". Precedent: past commits to `journal_validator.py` carry `tier: fable` / `tier: claude-fable-5-2` (`git log`, Trail).
A Sonnet builder can satisfy the DoD of A1, B0 or B23 only by writing a false tier line.
Fix: §2 and §4 say how these streams land. Either the builder hands over a commit-ready diff and a Fable session commits it with the axis block and the tier line, or the merge commit is the Fable act and the branch commits use the door the gate offers. In either case §5 moves the Fable time from "~1 h for L" to "every merge of A1/B0/B23".
C2 may use `axes: not a mechanism (a read-only CLI subcommand)` as §7 already says. Say so in its DoD.

## Should-fix (fix in the spec; not blocking the first wave)

- **S-1 (B23 item 1): the wrong reader for the model.** `dispatch_gate.LABEL_MODEL_PREFIX_RE = ^\S+[ :-]` is "Deliberately NOT a fixed list of model/tier names" (dispatch_gate.py:397-401). For the description "fix flaky test" it reads `fix`, and the hook would write `model: "fix"`.
  E-B23-3's invariant holds only in the letter. The tier-word reader that already exists is `_LABEL_LEADING_TOKEN_RE` + `_model_family` (dispatch_gate.py:1033-1056).
  Fix: name those two. When there is no family, apply E-B23-3: no write, show the door.
- **S-2 (B1 D1): msvcrt locks are mandatory on Windows, so the "held by pid N" text cannot be read.** Experiment (Trail): byte 0 is locked with `LK_NBLCK` and `pid ts` written into it; another process's `open(p,'rb').read()` then raises `PermissionError [Errno 13]`.
  E-B1-3's refusal text, and any implementation that reads the pid BEFORE trying the lock, fail.
  Fix: lock a byte at a fixed offset far past the text (e.g. 4096; locking past EOF is allowed). Open with `O_RDWR|O_CREAT` and never truncate while contending. As an alternative, write `pid ts` into a sidecar file.
- **S-3 (B5 D1): `git rev-parse --git-common-dir` is relative to the CWD, not to the repo root.** From `tools/` it prints `../.git` (Trail). Resolved "against the repo root", that gives `C:/QAFactory/.git`. Two callers with different cwd or `--repo` would then lock DIFFERENT files, with no mutual exclusion.
  Fix: `git rev-parse --path-format=absolute --git-common-dir` (git 2.56 here). Add a row: "--repo pointing at a subdirectory".
- **S-4 (B0 owns): incomplete.** B0's witness runs `tools/test_journal_validator_merge.py` and holds E-B0-7's merge row, yet B0 does not own that file. That file also pins band behaviour (Grep `id_band|band_lines|suggested_band|BAND_`: test_compact_snapshot, test_journal_echo, test_journal_keys, test_journal_validator, test_journal_validator_merge, test_session_context).
  The file holding `piles.py --task` rows (`tools/test_piles*.py`, 13 files) is not owned. Neither is `tools/test_transcripts.py`, which tests `peer_note`, whose text B0 item 7 changes.
  Fix: add them to B0's owns, or name which `-k` rows of which file.
- **S-5 (B0 items 3/7): leftovers of the retired road.** `compact_snapshot.py:308-329, 539-547` still prints "next id t-NNN" from `journal_keys.next_ids(...).main` (max+1) and the band lines. After the switch that is a stale id: the counter is ahead.
  The validator's NOVELTY refusal (journal_validator.py:1285-1304) still tells the writer to open `id_band`.
  Fix: list both in B0 item 3. The snapshot names `journal_write.py next`, and the NOVELTY text names the writer.
- **S-6 (A1): the rule 10 duty of critic.md is missing.** Rule 10 of `.claude/agents/critic.md` says editing that file "requires running the exam in PROCESS/CRITIC_EXAM.md BEFORE the commit". `PROCESS/CRITIC_EXAM.md` does not exist on disk. Positive control: the same `ls PROCESS` lists `LEAD_RANKING_EXAM.md`. SIBLING_MAP axis 2 says the exam is generated by `critic-exam-gen`.
  §7 axis 2 says "n/a for all" and A1's DoD is silent.
  Fix: A1's DoD names the exam run, or the deviation the rule allows, plus the Runs-log line in the same commit. Correct the axis 2 line to "covered for M1: critic.md edit → critic exam duty".
- **S-7 (F-B4-1 (a)): the chosen gate has no owner.** §11 chose (a), yet no stream owns `claim_control_gate.py` or a new gate file. No node exists for the WARN→refuse switch, which is meant to happen "the day check 48 shows a week with no by-hand line".
  During the WARN phase, Edit/Write appends without the lock while hooks append under it. The Edit tool's stale-read check makes a lost line unlikely, but tail-anchored Edits will keep failing as hooks append.
  Fix: add the gate to B23, or to a node B4 of its own with owns/edges/test. Name the switch node in §2, with its trigger and its owner (the Lead).
- **S-8 (F-T1, both branches judged):**
  (a) needs the owner's word and a CARRIER for the exception. TESTING.md:117 «новый тестовый файл не создаётся» and :55 «нового тестового файла на новый скрипт». Yet A2's invariant E-A2-1 forbids touching any line of «### Бюджет». Name the stream and line that carry the exception (A2 with E-A2-1 relaxed for that one line, or L).
  (b) costs less than §9 claims. The only real overlap inside a wave is `test_dispatch_manifest.py` (B0 and C1, both wave 1). B0→B1 (`test_journal_keys.py`) and A3→B23 (`test_mechanism_gate.py`) fall in DIFFERENT waves. `test_worktree_sweep.py` is not owned at all.
  Under (b), only C1 moves to wave 2. (b) needs no exception to the written rule (P31), at the price of hosting tools' tests in neighbours' files. Both branches are executable once that is fixed.
- **S-9 (C1 wave): C1 is placed in the same wave as what it depends on.** §11 chose F-B2-1 (a), so C1 depends on B0's header grammar (`task:`/`node:`/`feature:` lines). C1's round-trip test ("printed text passes `check`") needs B0's `dispatch_manifest` change.
  Fix: C1 goes to wave 2, which also matches S-8 (b).
- **S-10 (F-ORD-1 (a)): the base branch of B1 is not stated.** B1 needs B0's code, but B0 must NOT merge before B1 is accepted (D6).
  Fix: B1's worktree is based on B0's branch tip. B0's merge is held until B1 is accepted, and the two merge back to back. If B1 is rejected twice, F-ORD-1 (b) applies.
- **S-11 (B1 E-B1-2): the letter refusal is too wide.** "A task id with another clone's letter → refused" applies to every `--task`. That blocks `accept`/`reject`/`returned` for a task delegated by the developer's other clone once the journals merge.
  Fix: limit it to ISSUING a brand-new id.
- **S-12 (dod_track sibling, rule 5 class completeness): §10 names `dod_track.py` but no stream owns or queues it.** `VERIFICATION_COMMAND_RE = pytest|python\s+-m\s+pytest|python\s+.*test` (dod_track.py:127-128) classifies `python -B tools/journal_write.py accept --run "python -m pytest ..."`, and any `accept` whose `--witness`/notes text holds "test", as a verification run. Its outcome then comes from the printed text.
  If the writer echoes witness text ("12 passed"), main_gate counts a green run that never happened in this command.
  Fix: B1 gets an edge "stdout never echoes witness or notes text; the outcome line is `journal: ... written`/refusal only", plus one row in `tools/test_dod_track.py`. Alternatively, queue a node with its owner.
- **S-13 (B23 item 5 / F-B1-3 (a)): the mechanism net will miss a transitive import.** `mechanism_gate`'s `test_transitive_import_closure_of_live_wiring_is_covered_by_mechanism_prefixes` will demand `tools/hop_metrics.py`: journal_hooks imports `_LAUNCH_RE`, and dod_gate is live. It is not in the item 5 list.
  F-B1-3 (a) imports `ai-packages/qa-factory/scripts/hooklib.py` into a live forge hook. A package edit to hooklib then changes a forge gate's behaviour (axis 3 is not "n/a for all").
  Fix: take the item 5 list from the closure test. In §7, write axis 3 as "covered for M3: hooklib imported by a live hook; a hooklib change re-runs test_journal_write".
- **S-14 (C3 step 10): the journal is copied without the lock.** Step 10 copies the root's journal bytes without the `journal` lock, so a concurrent hook append can be cut mid-write.
  Fix: steps 9-10 read the root's journal under `machine_lock("journal")`.

## Nits

- N-1: `ID_RE` accepts `t-0123` and `t-000`. A leading zero gives two spellings of one number. Add a row: canonical `%03d`, so the 4+-digit form has no leading zero.
- N-2: the first id of a new letter (no prior ids of that letter) is not stated for 9a'; the counter yields `t-001a`. That is fine, but state it.
- N-3: the owner wrote «123А» (Cyrillic, upper case); the plan uses ASCII lower case `a`. That is a reasonable technical choice and should go to the owner as «решила сама».
- N-4: A3 under `git commit --amend` measures only the delta against the amended commit. State it, or use `HEAD~1` when amending. The WARN is per commit, not per builder diff: a builder who commits tests separately gets a false WARN, but the door covers it.
- N-5: §6.1's builder text restates the volume rule ("added test lines ... do not exceed"). E-A1-1's own invariant says the role holds "a duty sentence + pointer". builder-rules 7d is a third restating carrier and no stream owns it. Under (b), say that 7d stays as is, or give it to A1.

## Answers per key

1. **Facts by trail.**
   - K2 holds: the journal is refused only as a literal write target (`_add_target` :1282-1291, `_decide_command` :1509-1519; probes in the Trail).
   - K4 holds, verified by running it: `closes:t-123a` → `('t-123', None)`, and `closes:t-123ab@codex` → `t-123`. Also `t-１２３` (fullwidth) matches CLOSES_RE and the validator's `TASK_ID_RE` (`\d`). E-B0-1 covers both.
   - K5 holds: `may_issue` accepts only `n == main` or the next id of the line's own band (journal_keys.py:337-347).
   - K7 holds for dod_gate (exit 2 paths :12-30, main :560-609). The parallel-hooks premise remains an estimate, as the plan says.
   - K9 is an estimate as stated: `_LAUNCH_RE` hop_metrics.py:89, `agent_id` in the dod_gate payload.
   - K4's census of files holding the id regex is right. My wider Grep found no further reader: collect_intake, dup_ratchet, hook_liveness_probe and transcripts hits were false positives (Trail).
   - §3.B5: the lock and counter in the common dir are sound, apart from S-3 (relative path) and S-2 (mandatory locks). One letter per clone is sound.
2. **Feasibility and parallel sessions.**
   - Sound: the races of two writers in one worktree (the lock), two worktrees (the counter in the common dir), the union merge (merge mode does not re-judge rule 9 on kept lines, validator :1812-1829), and a crash holding the lock (the OS releases it).
   - Broken by BL-1 (9a' vs reservation), BL-2 (lock scope), BL-5 (second-worktree `returned`), S-2 and S-3.
   - TEMPORAL: old bands and bare ids stay valid (E-B0-5). F-ORD-1 (a) is executable only with S-10.
3. **Edges.**
   - Mostly complete and in battery form.
   - Missing: the POSITIONAL lock-scope invariant (BL-2), the cmd.exe divergence (BL-3), the second-worktree stop (BL-5), the `--repo` subdirectory (S-3), the reserved-lower-id row (BL-1), amend (N-4).
   - Hook order: E-B23-7 and E-B23-8 are correct given dod_gate's exit-0-only write. A blocked stop writes nothing.
4. **Rule 10.**
   - All 37 axes are enumerated per mechanism.
   - Wrong lines: axis 2 (S-6) and axis 3 (S-13).
   - Missing mechanism: the F-B4-1 gate (S-7).
   - Detectors: checks 7, 11, 13, 27, 33, 37 and 46 exist in the protocol (Grep in the Trail); check 48 is new in L.
   - (d) is acceptable.
5. **Owned paths.** No overlap within a wave, apart from C1 under F-B2-1 (a) (S-9) and under F-T1 (b) (S-8). Self-activating files are handed over as `.proposed` (correct). Every stream has a witness command; B0's owns miss files (S-4). The `designer:` line is present in §4. The tier gate blocks the commits (BL-6).
6. **Fit to the owner's words.** Every ask is present: start (hook `delegated`) and end (`returned`) of a dispatch, accept (`accept --run`), skip (CLI plus the automatic designer skip), template (`dispatch_new`), `ci why`, wave merge, the volume rule in both roles with the TESTING link, the how-to section, and the commit-msg WARN.
   Additions beyond the words: the `via`/`session` fields, the letters registry, and the Edit/Write refusal. Each is justified by a typed fact or by P31. Nothing unasked is substantive.
7. **Cost and order.** The order is sound with S-9 and S-10.
   The line counts are low, an estimate: B0 more like 500-700 lines across 9 files plus 9 test files, B1 more like 700+.
   The Fable time is understated (BL-6). The saving claims are plausible and are measured by check 48 (a)-(e).

## Duplication and consistency (rule 18)

One finding: S-1, the wrong reader (a second, looser tier reader would come into use where `_LABEL_LEADING_TOKEN_RE` + `_model_family` exist).
Everywhere else the plan reuses one survivor: `_LAUNCH_RE` imported, the manifest cut, `_decide_command`, `dispatch_manifest.check`, and `append_jsonl_line`.
Grepped: `LABEL_MODEL_PREFIX_RE` and `_model_family` over `tools/*.py`; `CLOSES_RE =` over `tools/*.py`, which found the 3 pinned copies the plan names.

## Code quality (rule 18)

None found beyond the blockers. The plan has no code. Its prescribed algorithms were checked for correctness above (BL-1..BL-5).

## One road (rule 19)

- Bands are retired (one id road).
- CLI `delegated` stays as the door when the hook fails, and it reaches the same writer. That is not a second road.
- The WARN phase of F-B4-1 is a transitional second road. It is legal only with the named switch node of S-7.
- `wave.py` is THE merge road with a named fallback (F-C3-2 (a)).
- No exclusion lacking an owner's word, apart from F-T1 (a), which is correctly put to the owner.

## Queue lines (homes)

- Spec fix round for BL-1..BL-6 and S-1..S-14: the designer t-842 fix round, or a Lead edit (a continuation of the same task_id). Home: the plan file itself, §3 and §9-§11.
- S-12 (dod_track classification of writer commands), if not folded into B1: a finding in `plans/piles/forge/findings/`, with a row in an untaken forge batch. Owner: the Lead.
- S-6, the missing `PROCESS/CRITIC_EXAM.md` that critic.md rule 10 requires: a finding in `plans/piles/forge/findings/`, since the rule cites a file absent on disk. Owner: the Lead.

## Trail

Files read:
- the plan (whole, 1-791);
- `tools/journal_keys.py` 60-180, 280-410, 762-785;
- `tools/journal_validator.py` (Grep of rules 9/merge; 1795-1844);
- `tools/hygiene_gate.py` 75-95, 440-455, 1275-1295, 1505-1535;
- `tools/dod_gate.py` 1-60, 560-625;
- `tools/dod_track.py` 140-260;
- `tools/dispatch_gate.py` 175-190, 390-440, 1030-1060;
- `tools/mechanism_gate.py` 78-95, 211-275, 572-600, 855-870;
- `ai-packages/qa-factory/scripts/hooklib.py` 600-630;
- `.githooks/commit-msg` (whole); `.claude/settings.json` (hook entries via Grep); `.gitattributes` (journal lines);
- `docs/TESTING.md` 40-148; `docs/SIBLING_MAP.md` axis headings (Grep) and 36-66;
- `docs/tasks/critic-diff-brief.md` 37-46; `plans/builder-rules.md` 7d (Grep);
- `.claude/agents/builder.md` rule list;
- `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` checks 7/11/13/27/33/37/46/47 (Grep) and 198-215;
- `tools/critic_verdict.schema.json`.

Greps (positive controls):
- `t-\\d|t-\(\\d|t-\[0-9\]` -i over `tools/*.py`: 9 files, journal_keys.py hit (control). Wider `t-\(|t-\[|t-\\d|t-\{|t-%|"t-"|'t-'` -i: 29 files; the extra non-test hits were inspected and are false positives.
- `CLOSES_RE\s*=`: 3 copies (journal_keys, calibration_counts, session_context).
- `id_band|band_lines|suggested_band|BAND_` over `tools/test_*.py`: 6 files.
- `peer_note` over `tools/test_*.py`: test_journal_echo, test_journal_keys, test_session_context, test_transcripts.
- `LABEL_MODEL_PREFIX_RE` over `tools/*.py`.
- `critic.exam|critic_exam` -i: SIBLING_MAP:48 and calibration :425 name the file. `ls PROCESS` lists no CRITIC_EXAM; control: the same `ls` lists LEAD_RANKING_EXAM.md. Glob `**/*CRITIC_EXAM*`: none.

Runs and experiments (verbatim results):
- `CLOSES_RE` probe: `'closes:t-123a' [('t-123', None)]`; `'closes:t-\uff11\uff12\uff13' [('t-１２３', None)]`; `'x closes:t-123ab@codex' [('t-123', None)]`; `TASK_ID_RE fullwidth True trailing nl True`.
- Proposed `ID_RE` probe: `t-123 True, t-123a True, t-123A False, t-123ab True, t-123abc False, t-0123 True, t-000 True`.
- hygiene_gate `_decide_command('Bash', ...)`: `echo x >> logs/journal/dev1.jsonl` deny; the backslash form deny; the `^/` form deny (mutation); `type nul >> logs\journal\dev1.jsonl` deny; `echo ' >> logs\journal\dev1.jsonl '` → `(0, None)`; `python -m pytest -q ' & echo x >> logs\journal\dev1.jsonl '` → `(0, None)`.
- cmd.exe (scratchpad): `subprocess.run(r"echo ' >> logs\journal\probe.jsonl '", shell=True)` → `rc 0`, `written: True "'  '\n"`.
- msvcrt (scratchpad): byte 0 locked, other process read → `READ FAIL PermissionError [Errno 13] Permission denied`.
- git (scratchpad repos): ff merge with a dirty journal that extends origin → `error: Your local changes to the following files would be overwritten by merge: j.jsonl ... rc=1`.
- `git -C tools rev-parse --git-common-dir` → `../.git`; with `--path-format=absolute` → `C:/QAFactory/forge-repo/.git`; git 2.56.0.windows.2.
- `git log -- tools/journal_validator.py tools/dod_gate.py`: commits carry `tier: fable` / `tier: claude-fable-5-2`.

Not run: no test suites. This is a plan gate and there is no code under review.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "BL-1 rule 9a' (greater than every seen number) refuses ids reserved by next or pre-issued in a dispatch when a higher id lands first; replace with never-seen + jump cap",
    "BL-2 accept --run executes inside the journal lock as written; run and witness-file read before the lock, lock bounded to read-validate-append",
    "BL-3 --run with shell=True runs cmd.exe on Windows while hygiene_gate judges Bash; verified bypass echo ' >> logs\\journal\\x.jsonl '; run via bash -c or shell=False with metacharacters refused",
    "BL-4 C3 step 9 ff-merge always refused after the first wave (verified git refusal with dirty journal); step 8 branch -d before refresh; byte-copy dance under the journal lock and delete after refresh",
    "BL-5 record_returned misses a delegating session in a second worktree, marker pruned silently; search every worktree journal copy, measure stop cwd in step 0, WARN on prune",
    "BL-6 A1/B0/B23 paths are in MECHANISM_PREFIXES; Sonnet builder commits are refused by the tier gate; state the Fable landing for them and fix the cost line"
  ],
  "fixes": [
    "S-1 read the model via _LABEL_LEADING_TOKEN_RE plus _model_family, not LABEL_MODEL_PREFIX_RE",
    "S-2 lock a byte far past the pid text; open O_RDWR|O_CREAT without truncation",
    "S-3 git rev-parse --path-format=absolute --git-common-dir",
    "S-4 B0 owns test_journal_validator_merge.py, the test_piles file with id rows, test_transcripts.py",
    "S-5 compact_snapshot next-id and band lines and the validator NOVELTY text name the writer",
    "S-6 A1 DoD carries critic.md rule 10 exam duty; axis 2 line corrected",
    "S-7 give the F-B4-1 (a) gate and the WARN-to-refuse switch node an owning stream",
    "S-8 F-T1 (a) names the carrier of the TESTING.md exception; F-T1 (b) cost corrected: only C1 shifts",
    "S-9 C1 to wave 2 (depends on B0 header grammar)",
    "S-10 B1 based on B0 branch tip; B0 merge held until B1 accepted",
    "S-11 letter refusal only when issuing a brand-new id",
    "S-12 B1 edge: stdout never echoes witness or notes; dod_track row, or queue",
    "S-13 MECHANISM_PREFIXES additions from the closure test incl. hop_metrics.py; axis 3 line for the hooklib import",
    "S-14 C3 steps 9-10 read the root journal under the journal lock"
  ],
  "class_completeness": "Id-grammar readers: K4 census verified with a wider grep (no missed reader). Retired-road leftovers: compact_snapshot next-id and validator NOVELTY text not listed (S-5). Mechanism net: hop_metrics transitive import missing (S-13). dod_track sibling named but not owned or queued (S-12). Axis 2 and axis 3 lines wrong (S-6, S-13); other 35 axes enumerated and plausible.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-coordinator-offload-spec.md",
      "tools/journal_keys.py",
      "tools/journal_validator.py",
      "tools/hygiene_gate.py",
      "tools/dod_gate.py",
      "tools/dod_track.py",
      "tools/dispatch_gate.py",
      "tools/mechanism_gate.py",
      "ai-packages/qa-factory/scripts/hooklib.py",
      ".githooks/commit-msg",
      ".claude/settings.json",
      ".gitattributes",
      "docs/TESTING.md",
      "docs/SIBLING_MAP.md",
      "docs/tasks/critic-diff-brief.md",
      "plans/builder-rules.md",
      ".claude/agents/builder.md",
      "PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python CLOSES_RE probe on closes:t-123a", "result": "('t-123', None): false close confirmed"},
      {"command": "hygiene_gate._decide_command Bash on echo ' >> logs\\journal\\dev1.jsonl '", "result": "(0, None): allowed"},
      {"command": "subprocess.run(echo ' >> logs\\journal\\probe.jsonl ', shell=True) in scratchpad", "result": "rc 0, file written with content quote-space-space-quote"},
      {"command": "msvcrt.locking byte 0 then read from another process", "result": "PermissionError Errno 13"},
      {"command": "git merge --ff-only with dirty journal extending origin (scratchpad repos)", "result": "error: local changes would be overwritten, rc=1"},
      {"command": "git -C tools rev-parse --git-common-dir", "result": "../.git (relative to cwd)"}
    ]
  }
}
```
