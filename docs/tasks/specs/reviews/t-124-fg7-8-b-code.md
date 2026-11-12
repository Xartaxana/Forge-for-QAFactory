# t-124 — code critic, FG7-8 part B (B1 + B2 + B3): the words `commit` / `stash` / `go on` of gate A's test-repository question

Critic (Opus), 12.11.2026. Under review: the uncommitted diffs of worktrees `agent-a365d2def0628cb25` (B1 + B2) and
`agent-a06a045949100fa96` (B3), against `docs/tasks/specs/fg7-8-b-vcs-words.md` (the three Lead-decision sections
first, then §1-§3, then nodes B1-B3) and the measured facts of `reports/t-118-b0-2-git-measure.md`.

**Verdict: fit_with_fixes — 1 blocking finding (BL-1), 9 non-blocking fixes for the same round, 3 node proposals.**
The verdict is an input to acceptance; acceptance is the Lead's.

## Empirics first (driving `repo_words.run` on scratch repos)

Probe `scratchpad/t124/probe.py` (full path
`C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\f92520fc-f552-4e47-9d06-efbc3daae572\scratchpad\t124\probe.py`):
a fresh repo per case under `scratchpad\t124\repos\`, the package imported from worktree 1, a story at
`qa-factory/artifacts/T-1` with a readable `pipeline.json`, the door built by `vcs_changes` + `vcs_state_block` exactly as
`check_vcs` does. "before/after/undone" = `status --porcelain=v1 -z -uall`, `ls-files -s`, HEAD, `stash list`.
git for Windows 2.56.

| # | Case | What the returned text claims | Observed | Named undo executed |
|---|---|---|---|---|
| A | Commit: ` M a`, `M  b`, `MM m`, ` D d`, `?? c`, plus `A  qa-factory/x.txt` staged and ` M qa-factory/z.txt` | "committed 5 change(s) as 4eea857785f4"; pass on `test repository state: 4eea857785f4` | HEAD commit = `M a, M b, A c, D d, M m` exactly; after: `A  qa-factory/x.txt` and ` M qa-factory/z.txt` untouched | `git reset --soft 53011ed585e7` + `git read-tree 9b2c99e9191b`: porcelain, index (incl. `:m.txt`), HEAD all == before (True/True/True) |
| B | `MM m` + `?? c`, pre-commit hook exits 1 | "Git did not do it (exit 1): refused-by-hook. Your staged changes are as they were. Nothing is passed" | porcelain, index, HEAD == before (True/True/True); no record | (none needed: restored by the code's `read-tree`) |
| C | Stash: ` M a`, `?? c`, another staged entry `A  qa-factory/y.txt` in the index | "put 2 change(s) aside in git stash 945125c0f17e"; pass on the HEAD block | after: only `A  qa-factory/y.txt` (+ factory artifacts) left; stash subject "On main: qa-factory T-1: ...(stash)" | `git stash apply --index 945125c0f17e`: exit 0, porcelain/index/HEAD == before (True/True/True); `reminder_line` printed `now stash@{0}`; `git stash drop stash@{0}` emptied the list |
| D | Stale door: a new `?? e.txt` after the door was built | "Your repository changed since you were shown the list ... nothing was done" | before == after (porcelain, index, HEAD, stash): True | — |
| E | Timeout: pre-commit hook `sleep 40`, `timeout=4` | "did not finish in 4 s and was stopped; HEAD is 14db9e7f8a51 (was 14db9e7f8a51). A leftover `.git/index.lock` blocks git: ... remove that file yourself, then `git read-tree 212f1d5a1b10`" | returned after 5.6 s; `index.lock` present (never deleted); HEAD unchanged; index = the `git add` result (not before); 45 s later `hook-late.flag` absent (the hook's tree was killed); `tasklist` shows no `sleep` | `rm .git/index.lock` + `git read-tree 212f1d5a1b10`: exit 0, `a.txt`/`m.txt` index blobs == before, porcelain back to ` M a.txt`, `MM m.txt` |
| F | Stash, person entry `?? q[a]-factory/z.txt` (a legal Windows name), factory entry ` M qa-factory/z.txt` | "put 1 change(s) aside in git stash 15ac35b186af"; **pass recorded** | stash holds `A q[a]-factory/z.txt` AND `M qa-factory/z.txt`: the factory's own file was stashed; `qa-factory/z.txt still dirty after: False` | — (BL-1) |
| G | Same tree, commit | "A commit afe8a59b7c97 was made, but it does not hold exactly the changes you were shown, so nothing is passed. To undo it: `git reset --soft a2577d14d263, then git read-tree 1aeb6c96dde8`" | HEAD commit = `A q[a]-factory/z.txt`, `M qa-factory/z.txt`: the factory file was COMMITTED before the post-check caught it | text true, but one backtick span holds two commands joined by ", then" (F-4) |
| F' / G' | F and G with `GIT_LITERAL_PATHSPECS=1` in the environment | stash / commit of 1 change | stash holds only `A q[a]-factory/z.txt`; commit holds only it; `qa-factory/z.txt` stays dirty (True) | — |
| A'-D' | A-D re-run with `GIT_LITERAL_PATHSPECS=1` | same as A-D | identical results, every undo True/True/True | the proposed fix regresses nothing measured |

## Blocking finding

**BL-1 — a person path with pathspec glob characters makes `stash` take the factory's folder and record a pass; `commit` writes it into a commit before the post-check refuses.** Surface: the pathspec the executor hands git (`repo_words.py:183-185`, `_exec`'s environment `_env()` at `:61-62`). Git reads every path after `--` as a pathspec with glob magic: `q[a]-factory/z.txt` matches `qa-factory/z.txt` too (probe F/G above). I-2 ("never the factory's folder ... Any difference: nothing runs") is broken on the stash road with a recorded pass (the stash judgment at `:217-225` checks only the ref, the subject and that the digest changed — never the set taken), and on the commit road the factory file lands in a commit (caught only after the write, at `:207-212`). Neighbouring classes of the surface walked: magnitude (`*`, `**`, `?` are illegal in Windows names but legal on POSIX, which `_kill_tree` supports: a file named `*.orig` would match `qa-factory/**/x.orig`); nesting (`[`…`]` in a folder name, shown here); encoding (a POSIX name starting `:(` is pathspec MAGIC — `:(top)`, `:(exclude)` — same fix); empty/broken (none). The same pathspec reading sits in `vcs_changes`'s `ls-files -s -z -- <paths>` (`gate_preflight.py` modes read): there it can only over-block (a foreign 160000 mode), the safe side, but it is the same surface.
**Fix (hand to a builder as is):** `repo_words._env()` returns `dict(os.environ, GIT_TERMINAL_PROMPT="0", GCM_INTERACTIVE="Never", GIT_LITERAL_PATHSPECS="1")` (measured above: F', G', A'-D'); the argv the guard reads is unchanged, so `rule_pathspec`/`rule_stash` stay as they are; pass the same variable in `gate_preflight._git_raw`'s environment for the `ls-files` read (or only there via an `env` keyword). Add one row to `part_repo_words` (`test_gate_preflight.py`): a person `?? q[a]-factory/z.txt` beside a dirty `qa-factory/z.txt`, both words: commit/stash take exactly the person path, `qa-factory/z.txt` stays dirty; red on revert of the env line. Optional hardening in the same round: judge the stash on the set it took as the commit is judged on G12 (`git stash show --include-untracked --name-only -z <sha>` == `paths`), so a future mis-take is a refusal, not a pass.

## Non-blocking fixes (same round, one fresh builder)

- **F-1 (duplication, AR-24/AR-13):** `run` builds the decision text by hand (`repo_words.py:237-240`) with a replaced-lines tail of its own (`; earlier lines this one replaces: a | b`) beside the one writer `contract.person_decision` (`contract.py:579`, tail ` (replaces their earlier line: a; b)`), which the spec names (§3.4) and both other driver branches call (`driver_machine.py:2821`, `:2896`). Fix: `said = C.person_decision(option, " ".join(str(line).split()), replaced)`.
- **F-2 (duplication):** `gate_preflight._git_raw` (`:223-235`) is a copy of `_git` (`:210-220`) minus `.strip()`. Fix: `_git` = `raw = _git_raw(...); return None if raw is None else raw.strip()`; one env dict (also reused by `repo_words._env`).
- **F-3 (code quality):** `repo_words.run` is ~99 lines (`:148-246`), the commit and stash judgments inline with three nesting levels; `_failed` takes 12 positional parameters including the module `GP`. Fix: extract `_judge_commit(...)` and `_judge_stash(...)` each returning `(facts, problem)`; pass a small dict to `_failed`. Census unaffected (neither name matches `UNIT_NAME_RE`).
- **F-4 (text a person reads):** the landed-not-exact problem (`:211-212`) puts `_commit_undo`'s "`git reset --soft X, then git read-tree Y`" inside ONE backtick span — copied, it is not a command. Fix: two spans, as `done_line` does (`:289`).
- **F-5 (I-6, Q3 below):** a commit that landed but is not exactly the shown set, and a stash entry left by a failed stash (`:220-231`), are writes in the person's repository with no record of the person's word: they reach the conductor once (driver `failed`, CLI exit 3), and nothing is kept. Fix: record a REMARK (`waiver.py --remark --stage <door stage> --text <the person's line; what landed; the undo>`) exactly as the `still` branch does, nothing passed.
- **F-6 (AR-1, one producer of the id):** `FINDING_ID = "vcs-test-repo"` (`repo_words.py:34`) is a second producer of the finding id that `Rehearsal.add` builds from check + subject; `_own_door` prints it. Fix: `run(..., finding_id=...)` given by both callers (the driver's `entry["id"]`, the CLI's stored-door key); drop the constant.
- **F-7 (Q1):** the undo command rides the prefix `the fix:` — for a successful action a person reads "the fix: undo it with ..." as if something broke. Fix: add an action prefix row `to undo it:` / `to take them back:` to `references/human-text.json` `action_lines` (data, AR-1) and use it in `done_line` / `reminder_line`; the Lead adds that file to the builder's owns.
- **F-8 (Q2):** the Q-1 clause yields "take exactly these:, files outside your tests folder included". Exact text: `your uncommitted changes ({total}), files outside your tests folder included, all listed - {words} take(s) exactly these:` (clause before the colon; the plain form unchanged when `outside == 0`), in `gate_brief.finding_door_hint`.
- **F-9 (minor, AR-28):** `vcs_changes` turns a failed `status` read (`_git_raw` → None) into "no entries"; after a write, `run` then reads `after["person"] == []` as clean and `unread` stays False (`:203-204`). Fix: return `None` from `vcs_changes` when `raw is None` (so `check_vcs` writes no finding, `run` refuses before, and after a write the result is `unread` → remark). Today's code had the same direction before the change, so this is not blocking.

## Node proposals (owners: the Lead opens them, rule 6)

- **N-1 (F14, Q7):** on the driver road the done line never reaches the person right after the action when the gate passes cleanly (confirmed: the clean-pass branch `driver_machine.py:3521-3535` never reads `stand["note"]`; only `_unread_kept_gate` at `:3542` does). Smallest carrier: a state key the person-facing gate text already reads — the `gate_note` carrier (`driver_gates.py:292-296`, written today by `driver_s0.py:616`) generalised to a list `person_notes` read and cleared by the next `Stop`/question builder; the clean-pass branch moves `repo_done_lines` into it. Per F14 (a) this is node (b); the end-of-run reminder already reaches the person.
- **N-2 (sibling of BL-1 outside the diff):** `stage_guard.rule_stash` / `_names_factory` (`stage_guard.py` ~`:2399-2442`) judge only literal path text; a glob path (`*`, `q[a]-factory/x`) passes and a real `git stash push -- '*'` by the orchestrator takes the factory folder. Fix there: refuse a pathspec carrying `*?[` or a leading `:(` unless the command sets `--literal-pathspecs`; axis: the guard's "never the factory folder" row.
- **N-3 (duplication, queue):** two `-z` porcelain parsers now exist: `gate_preflight._vcs_entries` (rename kept as a pair) and `test_repo_base.parse_status` (`test_repo_base.py:127`, rename flattened, `--branch` trick against the strip). One should read through the other (AR-13).

## The seven open questions — decision proposals

1. `--soft`/`--index` on a `the fix:` line: works, but wrong words for a person; take a data prefix in `human-text.json` (F-7).
2. Exact text in F-8.
3. Landed but not exactly the shown set: no pass and the undo named is right; the factory must not reset on its own. Add the REMARK (F-5) and fix the backticks (F-4).
4. `still`: keep exit 0 — the write happened, the remark is recorded, the printed text says nothing is passed and the question comes again; exit 3 would tell the conductor "nothing was done", which is false.
5. Stash timeout with a stale lock, no `read-tree`: right. Stash takes only `??`/` M`/` D` entries, so the index holds no person split to restore, and git stores the ref before it cleans the tree (a stored ref is judged as done or "entry left"). One nit: `_failed` says "your changes were not moved" without comparing the tree; acceptable.
6. Real mis-take, measured (probe F/G): must not run. Fix with `GIT_LITERAL_PATHSPECS=1` (BL-1), not a blocker row (a blocker would refuse legitimate `[draft].md` files on Windows).
7. N-1.

## Standing questions

- **Fit to the spec:** `run` steps 1-8, `main` (both forms), driver changes, census: present and traced (report §"run steps" spot-checked against the code). B1 items 1-8 minus the deferred `factory_origin` / F13 info row (absent, per the t-119 decision — not a finding). The seven B0-2 decisions: (1) stash blockers = any X not ` `/`?`, mode 160000, `.gitmodules` — `vcs_blockers`; ` A` blocks both; (2) drop by `stash@{N}` — `_stash_undo`, `done_line`, `reminder_line` (probe C); (3) commit undo (probe A); (4) subject equality — `reminder_line:316-323`; (5) tree kill, temp files, lock never deleted (probe E); (6) rename NEW then OLD (`_vcs_entries`), G12 OLD then NEW (`_names` collects both), `rev-parse` by exit code (`_git_raw`); (7) hook-created files → `still` remark. B3 bullets all present except two `conductor.md` clauses dropped for the 12 000-byte cap.
- **conductor.md cap:** dropped "run nothing" (it stands in the conductor-actions row and s4.md) and "the note section 'Done in the person's repository' is told line by line" (the section's own heading, `driver_machine.py` `_relay_note`, carries "tell the person each line as it stands" where the conductor reads it), plus the label's example list and the word "whole". Nothing load-bearing lost.
- **Invariants I-1..I-8:** I-2 broken by BL-1 (glob); I-6 "action with no record" open in two failure branches (F-5); I-3, I-4, I-7, I-8 hold on every traced and probed input (exact word only for writing rows, `?` refused, hooks run, no `--no-verify`/`-c`, unreadable pipeline closes, every undo measured true).
- **ARCHITECTURE:** AR-1 (grep `"commit"|"stash"|"go on"` in `repo_words.py`, `gate_preflight.py`, `gate_brief.py`, `driver_machine.py`: only git argv verbs and `vcs_blockers`' verb keys in the new code; the `driver_machine.py` hits at `:141`, `:2142` are older, other questions); AR-13 (F-1, F-2, N-3); AR-14 (`keep_shown_doors` one writer, both roads); AR-19 (one executor, `repo_words.run`, both roads); AR-20 (census `safety` 54 -> 55, row `repo_words.py run` safety/intent, nothing else moved: read in the diff); AR-28 (F-9); AR-29 (`run` is a safety check on repository state, no judgment of a role's output: `judgment: none` holds). `driver-layers.json`: row `shown_doors` removed (its writer/reader moved to `gate_brief`), `Driver._repo_reminder` and `repo_done_lines` added — named in the B2 report.
- **JUDGMENT:** none moved into code; census row read; no `blocks_override`, no scan-constant edit.
- **ONE ROAD:** one executor and one shown-doors store on both roads; Q-1 product code is the owner's open question with the Lead's interim (a), carried as a clause, not an exclusion. None found beyond: grep of `executor`/`writes_repository` consumers.
- **DUPLICATION AND CONSISTENCY:** F-1, F-2, N-3; `repo_words._env` duplicates `_git`'s env dict (folded into F-2). Grepped: `def _git`, `status", "--porcelain`, `person_decision(`, `def project_root_of`.
- **CODE QUALITY:** F-3 (`run` `:148-246`, `_failed` signature); F-4; no dead branch found.
- **TESTS:** the B2 table catches the defects it lists (red-on-revert list attached); it has no glob-path row (BL-1 adds one).

## Class completeness (axis 5, axis 34)

Axis 5: the map row "Gate A test-repository words" is node B4 (the Lead's, after B1-B3) — not built yet, by plan. Twins walked: `check_stand`'s and the clean-branch literal and the evals' old words are queued as B5 (spec §4); `halts.md` updated; "Carriers of a person's words" row: the CLI reads through `person_words.read` and prints `person_words.door` (kept); "One question for every stop": no new `Person`/`Stop`. New sibling found: N-2 (`stage_guard` glob pathspec). Axis 34: one executor, one store, two roads — holds.

## Trail

Read: the spec whole (855 lines); `repo_words.py` whole; the full diffs of both worktrees; `reports/t-123-b2-repo-words.md` whole; `reports/t-122-b3-texts.md` (grep of witness/cap lines); `contract.py:570-599`; `test_repo_base.py:88-140, 240-270`; `driver_machine.py:3340-3364, 3470-3545`; `gate_brief.py:3070-3099`; `gate_preflight.py:6147-6196`; `waiver.py` flags; `driver_runner.py:282-296`; `docs/SIBLING_MAP.md` axis 5 rows 111-145, axis 34 heading; `docs/tasks/critic-diff-brief.md:25-101`; `tools/critic_verdict.schema.json`.
Reruns (verbatim tails): `python -B <W1>/ai-packages/qa-factory/scripts/tests/test_gate_vocabulary.py` -> `=== test_gate_vocabulary: 141/141 ok ===`; `python -B <W1>/.../tests/test_gate_question_form.py` -> `=== gate question form: 297/297 ok ===` (both equal the B2 witness). Probe runs: cases A-D, F, G, F', G', E, A'-D' as in the table.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "BL-1: a person path with pathspec glob characters (probe: ?? q[a]-factory/z.txt beside a dirty qa-factory/z.txt) makes stash take the factory folder and record a pass, and makes commit write the factory file into a commit before the post-check refuses (repo_words.py:183-185, _env at :61-62). Fix: GIT_LITERAL_PATHSPECS=1 in repo_words._env and in gate_preflight._git_raw's environment; a part_repo_words row for both words; optional: judge the stash on the set it took."
  ],
  "fixes": [
    "F-1: use contract.person_decision(option, line, replaced) for the decision text instead of the hand-built string at repo_words.py:237-240",
    "F-2: gate_preflight._git delegates to _git_raw and strips; one env dict reused by repo_words._env",
    "F-3: split repo_words.run (:148-246) into _judge_commit and _judge_stash; give _failed a small dict instead of 12 positional parameters",
    "F-4: the landed-not-exact problem prints the undo as two backtick spans, not one span joined by ', then'",
    "F-5: a landed-not-exact commit and a stash entry left by a failed stash record a REMARK with the person's line, the facts and the undo, nothing passed",
    "F-6: drop FINDING_ID; run takes finding_id from its caller (driver entry id, CLI stored-door key)",
    "F-7: a data prefix 'to undo it:' / 'to take them back:' in references/human-text.json action_lines replaces 'the fix:' in done_line and reminder_line",
    "F-8: finding_door_hint first line with outside > 0 reads: your uncommitted changes (N), files outside your tests folder included, all listed - <words> take(s) exactly these:",
    "F-9: vcs_changes returns None when the status read fails, so a failed read after a write is 'unread' (remark), never 'clean'"
  ],
  "class_completeness": "Axis 5: map row is node B4 (Lead, after B1-B3); clean-branch literal, check_stand and evals queued as B5 by the spec; halts.md updated; person_words carrier row kept; no new Person/Stop. New sibling outside the diff: stage_guard rule_stash/_names_factory accept glob pathspecs (node N-2). Axis 34: one executor repo_words.run and one shown-doors store keep_shown_doors/shown_doors_of on both roads - holds. Duplication queue: two -z porcelain parsers (gate_preflight._vcs_entries, test_repo_base.parse_status), node N-3. F14: done line not delivered on a clean driver pass, node N-1 (carrier: a person_notes state key read by the next stop, beside gate_note).",
  "trail": {
    "read": [
      "docs/tasks/specs/fg7-8-b-vcs-words.md (whole)",
      "worktree agent-a365d2def0628cb25: git diff HEAD (all 12 files) and ai-packages/qa-factory/scripts/repo_words.py (whole)",
      "worktree agent-a06a045949100fa96: git diff HEAD (6 files) and changelog.d/fg7-8-b-vcs-words.md",
      "docs/tasks/specs/reports/t-123-b2-repo-words.md (whole); t-122-b3-texts.md (witness and cap lines)",
      "scripts/contract.py:570-599; scripts/test_repo_base.py:88-140,240-270; scripts/driver_machine.py:3340-3364,3470-3545; scripts/gate_brief.py:3070-3099; scripts/gate_preflight.py:6147-6196; scripts/driver_runner.py:282-296; scripts/waiver.py flags",
      "docs/SIBLING_MAP.md axis 5 (111-145) and axis 34 heading; docs/tasks/critic-diff-brief.md:25-101; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <W1>/ai-packages/qa-factory/scripts/tests/test_gate_vocabulary.py", "result": "=== test_gate_vocabulary: 141/141 ok === (equals the B2 witness)"},
      {"command": "python -B <W1>/ai-packages/qa-factory/scripts/tests/test_gate_question_form.py", "result": "=== gate question form: 297/297 ok === (equals the B2 witness)"},
      {"command": "python -B scratchpad/t124/probe.py a b c d", "result": "A commit exact + undo restores porcelain/index/HEAD True/True/True; B hook exit 1 restored True/True/True; C stash + apply --index True/True/True, drop by stash@{0}; D stale door refused, unchanged True"},
      {"command": "python -B scratchpad/t124/probe.py gs gc gsl gcl e", "result": "glob stash took qa-factory/z.txt with a pass; glob commit committed it, then refused; with GIT_LITERAL_PATHSPECS=1 both took only the person path; timeout 4 s: returned in 5.6 s, index.lock kept, hook tree killed, rm lock + read-tree restored the index"},
      {"command": "GIT_LITERAL_PATHSPECS=1 python -B scratchpad/t124/probe.py a b c d", "result": "identical to the run without the variable: every undo True/True/True"}
    ]
  }
}
```
