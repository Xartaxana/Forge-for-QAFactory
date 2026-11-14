# t-865 — critic, offload topic B (B0 t-850 + B1 t-861): journal schema and the one journal writer

Reviewer: critic (Opus 5.5). This is the verdict layer only. The mechanical layer was attached by the Lead, and I re-ran the cheap parts (see Trail).
Spec under review: `docs/tasks/specs/20261114-coordinator-offload-spec-r2.md`: §3.B0, §3.B5 D1-D6, §3.B1, §7 (b) and §11'.

## Verdict: GO WITH FIXES

Nothing blocks the design itself. B0's grammar, rule 9a'', the retired bands, `returned` and the readers fit the spec, and so do B1's
write order, lock, witness road and exit codes. Before B1 merges, three major defects need a fix round: F1, F2 and F3.
F3 turns `forge-check` red as soon as the branch lands. F1 is a permanent dead end for any second developer once the ids pass 1000.
F2 is a race between two sessions on Windows that reports "nothing written" for a line that was in fact written.
Minor items F4-F9 can go in the same fix round.

## Findings

**F1 (major): the first-use counter scan reads every developer's journal, so the writer can issue ids the validator refuses forever.**
`tools/journal_write.py:247` (`scan_worktrees`) globs `logs/journal/*.jsonl` (plus the history) in every worktree. Spec D2 asks for "the max
over every worktree copy" of THIS logical journal. Rule 9a'' (B0, `journal_validator.py:1347-1359`) measures the jump cap against the
max of the line's own logical journal. The two numbers disagree.
Probe (the scratchpad script, verbatim output): a clone with slug dev2 whose tree carries `dev1.jsonl` at t-1500.
```
P1 delegated rc 2 ... task_id='t-1501': task_id novelty violated -- got t-1501; it jumps more than 1000 above the sequence (no id exists yet) ...
P1 delegated rc 2 ... (same, second call)
P1 next (0, 't-1501\n')
```
`next` saves the counter at 1501, and the refusal text sends the user back to `next`. That loop has no exit except editing counter.json by
hand. The live journal is at t-864, so a developer who joins after about t-1001 hits it on their first call.
Fix: scan only `<wt>/<rel>` with `rel = jk.current_path(root)` and its seed. Reuse `read_journal` + `jk.max_by_letter(_objs(...))`, which also
removes the second line reader `TASK_IN_JSON_RE` (F8). Add a test row for the dev2 clone above: its first id is t-001.
The class around it: a counter that exceeds the validator's base. The same disagreement exists for two worktrees of one clone whose bases
are more than 1000 apart. Spec D4 accepts that case (the validator cannot see the counter), and a long-lived worktree makes it rare. Name it in
the module docstring as the known residual. The door is `event --json`.

**F2 (major): a failure after the append is reported as "nothing written", and on Windows the out-of-lock counter peek makes that failure
reachable between two sessions.**
- `journal_write.py:461-463`: `append_jsonl_line` runs, then `save_counter` (`:236-239`, `os.replace`). If the replace raises, the
  exception leaves the lock block and the catch-all at `:386-387` returns `written=False` with "...; nothing written". The line is in
  the journal and the counter has not moved.
- `journal_write.py:314` (`_pre_lock` → `load_counter` → `read_text`) reads counter.json OUTSIDE the lock. On Windows, `os.replace` onto a
  file that another handle has open fails. Probe (verbatim): `P2 replace while open: PermissionError [WinError 5] ... counter.json.11472.tmp -> ...counter.json`.
  So session B's peek can overlap session A's in-lock save.
- What follows: the caller, or a B23 hook, is told the write failed and writes again, which gives a second `delegated` under a new id. The
  counter now lags the file, so another worktree of the clone (whose file max does not see this line) can reissue the number. This is the
  owner's two-sessions requirement (Q4).
Fix: (a) everything after a successful append is reported as `written=True`, and a failure becomes a WARN ("counter not updated: <why>;
the next call takes max(counter, file)"). (b) Remove the out-of-lock read: decide in the lock whether a rebuild is needed (release, scan,
retake), or at least retry `os.replace` on PermissionError for up to about 1 s. Add a test row that monkeypatches `save_counter` to raise:
the line is present, `written` is True and the WARN is named.

**F3 (major, fix before merge): `tools/test_streams.py` S3 is red on the B1 branch.**
`journal_write.py:770-773` carries its own `.reconfigure` loop. journal_write is not in `MECHANISM_PREFIXES` (`mechanism_gate.py:239-271`
lists journal_echo, journal_validator and journal_keys, but not journal_write or journal_lock). Spec §7 (b) axis 15 says new CLIs set UTF-8 "through
the tools helper". Re-run (verbatim): `FAILED tools/test_streams.py::test_s3_no_tool_outside_the_chain_carries_its_own_stream_reconfigure`
-- "tools/journal_write.py calls .reconfigure( 1 time(s) outside the mechanism chain"; `1 failed, 39 passed`. The builder's witness
scope (its own test file only) could not see this.
Fix: call `streams.utf8_stdio()` after the bootstrap, as the spec says. The B23 node, which brings journal_write into MECHANISM_PREFIXES (S-13),
then applies the axis 15 closing rule: a link keeps its own copy, or the Lead brings streams.py into the chain. Write that into B23's DoD.

**F4 (minor): Q1, the test row does not tell the copy branch apart.**
`test_journal_write.py:343-350`: the main worktree's row has letter "" and the linked worktree's registry is emptied. If `others` is never read,
`used` is empty and the claim also yields "", so the test passes with or without the cross-worktree read.
Fix: in the main worktree registry, give this clone letter "a" and give another clone of slug dev1 letter "". The linked worktree's claim must
then print 'a'. This is one more row in the same fixture.

**F5 (minor): a typo on accept/reject/escalate/defect gets the wrong door.**
`journal_write.py:447-450` applies `_check_new_task` to every unseen task id. For `accept --task t-990` (a typo above the counter) the text is
"t-990 was not issued; take one from `next`". The right answer is the validator's orphan text: "point task_id at a real earlier delegated".
Fix: run `_check_new_task` only for novelty-issuing `delegated` and for `decomposable` (the validator does not orphan-check
decomposable). For accepted, rejected, escalated and defect_found, let the validator's text speak.

**F6 (minor): `returned` reads the journal outside the lock.**
`journal_write.py:675-682` (`_matching_delegated`) is a journal read that feeds a write, which D1 puts under the `journal` lock. It does no
harm today because the validator re-judges 9f inside the lock. Fold the lookup into the locked read of `_write_event`, or have the Lead record it
as an accepted deviation.

**F7 (minor): `--run` executes before the task id is checked.**
`journal_write.py:701-702` runs the witness (up to 600 s) before the grammar, existence and letter checks at `:447-450`. Spec step (1), "parse
and check the arguments", comes before step (2). Fix: an advisory, read-only pre-check of `--task` (grammar plus "seen or ≤ counter")
before `run_witness`. The locked check stays authoritative.

**F8 (minor, duplication): grammar pieces copied out of `journal_keys`.**
- `ID_GRAMMAR_TEXT` `journal_write.py:62` = the literal at `piles.py:3257`.
- The "not canonical" text `journal_write.py:411-412` ≈ `journal_validator.py:1352`.
- The letter grammar `[a-z]{0,2}` is restated at `journal_write.py:227` and in the letter enumeration at `:576`, against `journal_keys.py:80`. The same
  goes for `ID_NUMBER_MAX` (`:58`) and `fmt_id` (`:126`).
- `TASK_IN_JSON_RE` (`:70`, `:253`) is a second line reader next to `jk.split_lines` + `jk.max_by_letter`.
- The notes check is copied inside the diff: `:695-700` against `:395-400`.
Fix: move the texts, the letter enumeration and `fmt_id` into `journal_keys` beside `is_canonical`. Have piles and the validator import the texts.
The CLOSES_RE fallback copies in session_context and calibration_counts are named in the spec and pinned equal, so they are not a finding.

**F9 (minor, AR-22 analogue): fields with no reader.**
`calibrated --period / --events-reviewed` (`journal_write.py:631, 745-746`) write two new typed fields. No reader exists (grep
`events_reviewed|"period"` over tools/, CLAUDE.md and the calibration protocol finds only journal_write), and the spec has no row for them. Fix: drop them
(the period goes in notes, as on the live calibrated lines), or the Lead adds a spec row with a reader.

Seam note (not a finding against B1): deviation 5 leaves hook-written notes uncapped by the library. CLAUDE.md rule 12 caps journal notes
at 300, so B23's DoD must cap or cut the notes the hooks build.

## Answers to the dispatch questions

1. **Deviation 1 (claim copies the row across worktrees).** The design is right. The letter is a function of the clone id (D3: "a clone's letter =
   the row whose clone is its id"). Two worktrees share the common dir, and with it the clone id and the counter, so they must share one letter.
   Without the copy, a linked worktree branched before the row merged would take a new letter, and two rows with one clone id would meet
   at the merge. Writing the same row on both branches merges cleanly in git, because both sides make the same addition. The copy branch must get a
   test row that discriminates it (F4). The current row does not.
2. **Deviations 2-9 against spec r2 and §11'.** No contradiction. The lock byte at offset 4096, the holder at bytes 0-63 read unbuffered, and
   `--path-format=absolute` with the relative fallback resolved against `<dir>` (old-git echo handled by taking the last line) match D1/S-3. `--run` is judged
   by `hygiene_gate.run_allowed`, run as `[bash, -c]` after the capability probe, and run before the lock, which matches F-B1-4 (a) and BL-2. `returned`
   (writer: `agent`/`model` taken from the matching delegated) matches B0 item 4. Letters are lower-case ASCII `[a-z]{0,2}` per F-B5-2 (a). The
   owner's «123 и 123А» is kept as the concept, a letter suffix; the spelling is the Lead's recorded technical decision. Deviations 2, 3, 5, 6, 8 and 9 are in the safe direction.
   Deviation 4 adds an earlier refusal and leaves the validator as the judge. Deviation 7 is the right resolution of a spec defect (the
   dispatcher's): D1 ("every read of a journal copy that feeds a write" under the lock) and D2 (first use = max over every worktree copy) conflict
   with B1's invariant (no subprocess or foreign read under the lock), and the spec left that pair unresolved. The peek itself is what opens F2 on
   Windows.
3. **Writer against validator, one producer and one reader.** They agree on `returned` (required `task_id`/`worker_ref`/`model`, 9f open delegated
   with the same worker_ref; the writer's own refusal comes first and the validator decides), on `via` (cli/hook), on `witness_by`
   (run/file/text on accepted), on the absence of `id_band` (the writer never writes one), and on letters (both read through `jk.ID_RE`/`parse_id`/
   `is_canonical`; the existing-task test is the validator's own `extract_task_ids`). They disagree in two places. (i) The counter's id against the 9a''
   jump base, F1, where the writer issues what the validator refuses. (ii) Fields produced with no reader, F9. Duplicated grammar: F8. The clone ratchet reports
   `tools: 16 groups, 16 known, 0 new, 0 grown`.
4. **Two parallel sessions on one computer.** The lock, the in-lock read-issue-validate-append-save sequence, the concurrent first-use scan
   (the in-lock counter wins and the scan is only a fallback), the concurrent claim, and the clone-id creation (O_EXCL plus a wait) are all sound. E-B1-11
   (4 real processes) passes. One race is left: F2, the out-of-lock peek against the in-lock `os.replace` on Windows, shown by the probe above,
   with its misreport and duplicate-line consequence. Stated residuals that stay as they are: a hand-given id that is ≤ the counter and unseen in this
   worktree can reuse another worktree's id (E-B0-4, check 46). Edit/Write writers stay unlocked until B23-S (transitional, named in the spec).

## Standing questions (critic-diff-brief)

- 1 Fit: met except F1 (D2 scan scope), F3 (axis 15 helper) and F7 (order step 1).
- 2 Own decisions: see Q2. All are safe except the F2 window.
- 3 Seams: B1 adds 4 new paths and B0's tree is untouched. The B23 seams are F3's MECHANISM_PREFIXES/streams decision and the notes cap.
- 4 Class completeness: see the axis lines below.
- 5 Tests: 504 test lines against 986 product lines. Rows exist per E-B1-n. The gaps are F1, F2 (no row for their defects) and F4 (non-discriminating). No keep row
  is owed: `test-layers.json` is the package's carrier and deviation 8 is correct.
- 6 DUPLICATION AND CONSISTENCY: F8, F9. Clone ratchet: 0 new.
- 7 CODE QUALITY: no new function over about 60 lines (`_write_event` `:426-476` is 50). There is no deep nesting. Small dead weight: the `_Pre.forge` field is
  never read, and `show_letter` calls `clone_id` twice. The after-append misreport is F2. The platform choice is inconsistent: the lock picks by capability
  (an import), while `run_witness`/`_kill_tree` pick by `os.name`. That is harmless, and I note it only.
- 9 Ratchets: no in-tree ratchet row was added or raised by B1. B0's band-row rewrites are test rows, not ratchets.
- 10 ARCHITECTURE: this is not a package change. The forge analogue of AR-22 is Q3 (F1, F9). The AR-13 analogue (a fact with a reader function is
  read through it) is broken by `TASK_IN_JSON_RE` (F8).
- 11 JUDGMENT: none. The writer judges data shape only; legality stays the validator's.
- 12 ONE ROAD: none found. I grepped journal_write/journal_lock for language, project or slug branches: the only branches are platform process-control
  (`os.name`) and the capability import, and both reach the same mechanism. One id road (the counter) and one write road (the writer) are kept. The
  Edit/Write road is the named transitional WARN that closes at B23-S.

## SIBLING_MAP axes touched

- axis 1 (journal readers <-> task key): covered in code by B0 (all readers in the spec list read `jk.ID_RE`). The map row additions are §6.5's,
  queued to stream L.
- axis 3 (forge hook imports package hooklib): covered. `test_journal_write.py` exercises the appender. The map line is queued to L (§6.5).
- axis 6 (measurement learns new event): covered by B0 (forge_metrics, calibration_counts, compact_snapshot, session_context).
- axis 10 (path resolution through git): covered (`--path-format=absolute`, relative fallback against `<dir>`, steering variables dropped).
- axis 11 (judged grammar = run grammar): covered (`run_allowed`, then bash).
- axis 13 (one dispatch cut): covered by B0 (`designer_skip_reason`, `header_ids`).
- axis 15 (console streams): NOT covered. This is F3 (own copy outside the chain; the spec names the helper).
- axis 18 (ratchets): covered. Nothing raised; dup ratchet 0 new.
- axis 29 (one jsonl appender): covered in code (`hooklib.append_jsonl_line` under the lock). The adopter line in the map is queued to L (§6.5).
- axis 34 (one road): covered (see 12).
- every other axis: n/a. Neither stream touches package stage twins, story paths, judgment census, role tools or host receipts.

## Trail

Read:
- the spec r2 §3.B0, B5, B1 (241-445), §6.5 and §7 (798-891), and §9'/§11/§11' (920-1009);
- the handoffs t-850-B0.md, -r2.md, -r3.md and t-861-B1.md (whole);
- `tools/journal_write.py` (1-815, whole) and `tools/journal_lock.py` (1-171, whole);
- `tools/test_journal_write.py` 1-120 and 343-365, plus the test name list;
- `tools/journal_validator.py` 419-431 (`extract_task_ids`) and 1090-1368 (rules 9a''/9f, `_novelty_reason`/`_novelty_text`);
- `ai-packages/qa-factory/scripts/hooklib.py` 600-630 (`append_jsonl_line`);
- `docs/SIBLING_MAP.md` axis 15 (348-373) and the axis 29 paragraph;
- `docs/tasks/critic-diff-brief.md` 25-104; `tools/critic_verdict.schema.json`;
- `tools/mechanism_gate.py` (grep `journal_` → 239-271).

Greps:
- id-grammar literals over journal_keys, journal_write, piles, journal_validator, session_context and calibration_counts (`3-9 digits|ID_RE =|[a-z]{0,2}|999`);
- `events_reviewed|"period"` over tools/*.py, CLAUDE.md and PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md (only journal_write; positive control: the same grep hits journal_write:631);
- the live dev1.jsonl for the `calibrated`/`lead_restored` shapes (agent lead; categories calibration, process and coordination);
- `logs/journal/` in the B1 worktree: only `dev1.jsonl`, max t-860.

Re-runs (B1 worktree, B0 applied):
- `( cd .../offload-b1 && python -m pytest tools/test_journal_write.py -q -p no:cacheprovider )` → `77 passed in 36.67s` (matches the witness).
- `( cd .../offload-b1 && python -m pytest tools/test_streams.py -q -p no:cacheprovider )` → `1 failed, 39 passed in 5.10s` (F3).
- `( cd .../offload-b1 && python -B tools/dup_ratchet.py --check )` → `dup ratchet: tools: 16 groups, 16 known, 0 new, 0 grown, 0 carried, 0 shrunk/gone (0 diverged)`.
- Probe script (scratchpad `t865/probe.py`, run against the B1 tools) → the P1 and P2 output quoted in F1 and F2.

I did not re-run B0's 13-file set (198 s). The witness numbers are consistent with r3 and with the B0 report's E-row map, and both B0 files I read in this
review run inside B1's 77-row set. I wrote no code and did not touch CI.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Axes touched: 1, 3, 6, 10, 11, 13, 18, 29, 34 covered in code (map-row additions for 1/3/29 queued to stream L per spec 6.5); axis 15 NOT covered (F3: own reconfigure copy outside the mechanism chain, test_streams S3 red). Counter-vs-validator class (F1) also present for two worktrees of one clone more than 1000 apart: accepted residual per D4, to be named in the docstring.",
  "trail": {
    "read": [
      "docs/tasks/specs/20261114-coordinator-offload-spec-r2.md 241-445, 798-891, 920-1009",
      "docs/tasks/handoffs/t-850-B0.md, t-850-B0-r2.md, t-850-B0-r3.md, t-861-B1.md",
      ".claude/worktrees/offload-b1/tools/journal_write.py 1-815",
      ".claude/worktrees/offload-b1/tools/journal_lock.py 1-171",
      ".claude/worktrees/offload-b1/tools/test_journal_write.py 1-120, 343-365",
      ".claude/worktrees/offload-b1/tools/journal_validator.py 419-431, 1090-1368",
      ".claude/worktrees/offload-b1/ai-packages/qa-factory/scripts/hooklib.py 600-630",
      "docs/SIBLING_MAP.md axis 15 and axis 29",
      "docs/tasks/critic-diff-brief.md 25-104",
      "tools/mechanism_gate.py 239-271 (grep)"
    ],
    "reruns": [
      {"command": "python -m pytest tools/test_journal_write.py -q (offload-b1)", "result": "77 passed in 36.67s"},
      {"command": "python -m pytest tools/test_streams.py -q (offload-b1)", "result": "1 failed, 39 passed: test_s3 journal_write.py reconfigure outside the chain"},
      {"command": "python -B tools/dup_ratchet.py --check (offload-b1)", "result": "tools: 16 groups, 16 known, 0 new, 0 grown"},
      {"command": "scratchpad t865/probe.py (dev2 clone with dev1.jsonl at t-1500; os.replace onto an open file)", "result": "delegated rc 2 jump refusal twice, next printed t-1501; PermissionError WinError 5 on replace"}
    ]
  },
  "fixes": [
    "F1 major journal_write.py:247 scan only this developer's logical journal (jk.current_path + seed) per worktree; test row dev2 clone first id t-001",
    "F2 major journal_write.py:461-463 and 314: a failure after append is written=True with a WARN; remove the out-of-lock counter read or retry os.replace on PermissionError; test row save_counter raises",
    "F3 major journal_write.py:770-773 use streams.utf8_stdio() per spec 7(b) axis 15; B23 DoD carries the chain decision when journal_write enters MECHANISM_PREFIXES",
    "F4 minor test_journal_write.py:343-350 make the linked-worktree claim discriminate (this clone letter a, another clone letter empty)",
    "F5 minor journal_write.py:447-450 apply _check_new_task only to delegated and decomposable",
    "F6 minor journal_write.py:675-682 move the returned lookup under the lock or record as accepted deviation",
    "F7 minor journal_write.py:701-702 advisory read-only --task pre-check before run_witness",
    "F8 minor move ID_GRAMMAR_TEXT, the canonical text, letter enumeration, fmt_id into journal_keys; replace TASK_IN_JSON_RE; dedupe the notes check 395-400 vs 695-700",
    "F9 minor journal_write.py:631,745-746 drop period/events_reviewed or add a spec row with a reader"
  ]
}
```
