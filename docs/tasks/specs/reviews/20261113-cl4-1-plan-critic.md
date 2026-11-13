# CL4-1 plan critic: review of the draft spec `20261113-cl4-1-collect-stalled-looped-spec.md`

Critic (Opus), 13.11.2026. Critic-on-PLAN: no code exists yet. Facts were checked on `.claude/worktrees/read-main` at **e4ba384**
(`git log -1` = "e4ba384 wave 1 integration report"). The designer read the root checkout at f52faed, which is **95 commits behind**
(`git log --oneline f52faed..e4ba384 | wc -l` = 95). Every file:line below is on read-main.

**Verdict: fit_with_fixes.** The direction is sound. Two findings block dispatch (B1 money, B2 a self-contradicting acceptance
rule that also breaks FR-41), and eleven amendments follow. All of them are spec edits the Lead can apply: none reopens the
design, so the designer is not needed again (§ "Who applies" below).

---

## 1. Facts (§0): true on e4ba384?

Files that did not change between f52faed and e4ba384 (diff with `--strip-trailing-cr` = 0 lines): `collect_stall.py`,
`collect_pack.py`, `driver_gates.py`, `references/collect-loops.json`, `test_probe_gap_door.py`, `test_probe_not_proved.py`,
`SKILL.md`, `tools/collect_intake.py`, `tools/test_collect_intake.py`, `kb/04-onboarding-doctor.xhtml`, `docs/TESTING.md`,
`plans/builder-rules.md`. So C1-C11, C16-C18, C20, T5, T6 and N3's lines all hold. I re-read C1 (`_l_records` 373-417), C2 (:380,
:393), C3 (:156-168), C4 (:337-340), C5 (:495-499), C6 (:515-516, :530-532), C7 (`collect_pack.py:1118-1131`), C8
(`collect_intake.py:662-679`), C10 (`collect_pack.py:1071-1072`, :1108-1117), C16 (:208-213), C17 (`collect-loops.json:10-17`,
`collect_stall.py:725-775`) and C18 (:72-74). Every one is correct.

Files that changed: `driver_machine.py` (112 diff lines), `driver_runner.py` (96), `driver_dispatch.py`, `test-layers.json` (71),
`test_story_run_loop_b_loop.py` (1 line, :69), `judgment-census.json`, `SIBLING_MAP.md`, `test_driver_stop_record.py`.

**Stale references (correct value on e4ba384):**

| Spec ref | Says | Is |
|---|---|---|
| C12 | `window_round_gate` `driver_machine.py:316-403` | **:319-414** |
| C12 | stop append + `save_state` :359-362 | **:363-365** (the dedup `if not any(...)` is :363) |
| C12 | question state `{"why": "threshold" ...}` :381 | **:384** |
| C12 | `self.no_move(state)` :401 | **:404** |
| C12 | `to_conductor` append + `save_state` :402-403 | **:405-406** |
| C12 | `WINDOW_ROUND_CAP = 2` :44 | **:45** |
| C13 | outcome words :358, :361, :402 | `same_set`/`cap` **:361**, `to_conductor` **:405** |
| N1 edges | the empty-set edge `:327-329` | the early return is **:344-345** (docstring EDGES :330-332) |
| C15 | `journal_run` `driver_runner.py:402-414` | **:407-419** (`_open_calls` :412-419) |
| N1 given | `driver_machine.py:302-410` | **:305-415** |
| T1 | quarantine section starts `test-layers.json:7067`; entries :7500, :7517 | **:7126**; `test_collect_pack.py` **:7559**, `test_collect_stall.py` **:7576** |
| T4 | `test-layers.json:5730` (`test_story_run_loop_b_loop.py` keep row) | **:5789** |
| T4 | `slow_tests.json:136` (58.4 s) | value right, path is `ai-packages/qa-factory/scripts/slow_tests.json:136` (not `scripts/tests/`) |
| R5 / N1 builder check (a) | the module list of `driver-runs.jsonl` readers | **incomplete**: on e4ba384 the readers are `collect_stall, dispatch_liveness, driver_conductor, driver_journal, driver_machine, driver_runner, driver_timing, factory_dashboard, friction, infra_failure, retro_numbers, run_counters, story_budget, story_progress, story_run, task_price, walk_timing`. The list is missing **`task_price.py`** (reads through `DJ._journal_paths`/`DJ.read_rows`, so a grep for the file name misses it) and **`run_counters.py`** (new on main) |
| N1 step 3 | "seen only through L1/L5/L7" | L7 reads only the `repair_limit`/`exit_limit` question rows (`collect-loops.json:16`). The window-cap question is `kind: refusal` (R2), so L7 never sees it. The current docstring's "L1/L5" is the right one |
| N1 step 3 / F-7 | "an older driver cannot be told from one whose windows never capped" | false as stated: every manifest story carries `plugin_version` (`collect_pack.py:1071`, `story_version.plugin_version_of`). What is true: the version in which the row first ships does not exist yet (temporal) |

**A fact §0 does not have (it changes N1):** since f52faed, `Driver.run` writes `kind: "process"` rows into `driver-runs.jsonl`
(`driver_machine.py:1776-1828`, `driver_journal.process_start_row/process_end_row` :552-588). There is now a precedent filter in
the test N1 edits, `test_story_run_loop_b_loop.py:69` (`r.get("kind") != "process"`). That test is S1 only, so a `window_round`
row never reaches it.

**Negative claim verified (T3: no keep row covers `collect_pack.py`):** a Grep for `"collect_stall.py"` in `test-layers.json`
finds `:1418` (the positive control, same shape). On read-main, `test_collect_pack.py` appears only in `quarantine` (:7559). The
designer's negative holds.

**My own negative, with a positive control:** "no reader routes the pair (stalled, looped) other than the sites the spec names."
A case-insensitive grep for `looped|"stalled"|get(.stalled.)` in `collect_pack.py` and `tools/collect_intake.py` (positive control:
it finds the known sites :1129-1130 and `collect_intake.py:665`) also finds **`collect_pack.py:1116`**:
`if item["looped"] is None and not verdict.get("stalled") and verdict.get("loop_unreadable_reasons")`. That is a pair decision the
spec does not list. The AR-13 grep in N2/N4 (`get("looped"`) cannot see it, because it reads `item["looped"]`. See A2.

## 2. Feasibility (§2): stalled or looped visible on every road, unknowns as unknown

- **A story that never finished:** stall half unchanged (K1-K7, `current`). Visible as today.
- **A window that capped and then closed:** this is what M1 fixes. The journal row survives the pop (W4 is a real driver →
  real `judge` join, `driver-runs.jsonl window_round row cap|same_set`). Feasible as designed.
- **A loop under the window-round cap:** by the existing rule this is not a loop ("Exceeded caps only (a cap exactly reached is not
  a loop)", `collect_stall.py:74-75`). The L2 values `["cap", "same_set"]` keep that. The extra critic dispatches still reach L1
  (`max_normal` 2, `collect-loops.json:3-8`). Consistent; not a gap of this spec.
- **A story with no transcript:** `select_transcripts` returns a gap or "no transcripts: …" (`collect_stall.py:521-524`), and the
  packer writes the H gap with the state word (`collect_pack.py:1128-1131`). Feasible. The new state word for an unknown stall is
  wrong, though (B2).
- **Unknowns reported as unknown:** this fails in two places. (i) N2 words `stalled` UNKNOWN as "stalled" (B2). (ii) F-7(a) leaves a
  pre-row story's closed capped window as `looped: false`, and nothing in the output names the blind spot (A9). The rest holds:
  `looped` None packs, and the intake renders `unknown`.
- **What leaves the project:** M1 widens the set of stories whose transcripts are packed. A story whose only loop evidence is a
  capped and since-accepted window used to be `looped: False`, which meant no transcripts. With M1 it is `looped: True`, and its
  transcripts go into the package. The owner's word covers the class: `release-next/findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md:9`,
  "брать ли транскрипты и у стори с петлями (повторные диспатчи, исчерпанный кап)" — «да, брать», владелец 30.10.2026. So this is
  not an owner fork. But the spec does not name it: §6 axis 14 says "transcript selection is unchanged … equal results for real
  verdicts", which is true of M2 only. The changelog fragment and the KB "Send" row do not say it either. See A6.

## 3. Architecture (§1)

- **AR-1 / FR-13:** kept. L2 is a data row, and `load_loops` (`collect_stall.py:725-775`) accepts it: shape `rows`, carrier in
  `JOURNAL_FACTS`, `kind` a word, `values` a non-empty word list. The reused id L2 has a precedent (L4 twice). **But** a second
  closed table of journal kinds exists, and the spec misses it: `references/driver-journal-kinds.json` `no_call_kinds`, the data row
  every no-session kind must have (B1).
- **AR-13 / AR-15:** one reader of the pair (`loop_state`) is right. It is incomplete without `collect_pack.py:1116` (A2).
- **AR-14:** kept. The row goes through `journal_run` → `_append_jsonl` (`driver_runner.py:407-409`).
- **AR-22:** `window_round` has a producer (N1) and a reader (L2) in the same commit. `ignored`/`loop_ignored` have a producer
  (`judge`), a carrier (N4 `_stall`) and a reader (N4 intake). Kept. The row's extra fields (`stage`, `key`, `round`, `cause`,
  `findings`) have no reader except the tests. That is acceptable for a journal row (the sibling `gate_repair` has the same), but
  §1 should say it in one line.
- **AR-4:** kept. `findings` is a count, not the set. `key` is `<stage>|<case keys>` and `dispatch` an id. No host path or machine
  name is written.
- **AR-28:** see B2 and A9.
- **AR-29:** kept (§6 below).
- **Privacy of `ignored`/`loop_ignored`:** these add no new class of content. Each `where` is built by the same f-strings as the
  signals' `where`, which already travel (`collect_stall.py:193, 201, 255, 268, 284, 299, 359, 380, 433`). One note: L5's `where`
  carries `match[:60]`, a stage-override block text from the project (:433). It already travels for L5 signals; now it also
  travels for L5 records with no time. §2.4 or N4 should say "the same strings as the signal `where`s, nothing more" in one line.
  Whether the manifest passes the redactor was not checked by me. Name it as an N4 builder check (A6).

## 4. Error direction of reused functions; adversarial inputs

- `journal_run` in a new caller: its `OSError` is uncaught, the same as the sibling (`driver_gates.py:822`). It errs toward a
  loud stop. Acceptable.
- `wants_transcripts` → `loop_state` (F-5): the gate errs only toward packing. Right.
- **`_rows_without_session` (`task_price.py:561-585`), reused implicitly by N1's new row: it errs toward `incomplete`, which is the
  money side.** This is B1.
- Outside data. The manifest at intake comes from other projects, and I1-I6 cover broken types, non-list values, non-dict entries
  and hostile bools. Missing is one row for a `where`/`why` that is not a string (None, int, nested dict). `"%s | %s"` renders it
  without a crash, but the spec should state that and test one entry (A10). Magnitude is bounded by the existing `part_max_bytes`.
  No new limit, so no AT/BEYOND row is owed. Encoding: the `csha` encodes with `"replace"` (`collect_intake.py:586`), and the raw
  render of control bytes is in §7 (candidate finding). Acceptable.
- Journal with no window rows → no L2 signal (temporal before). A torn tail → the existing `_jsonl_rows`. A broken middle line → an
  existing reason, so `looped` None. Covered.
- Broken, empty or huge transcripts: this spec does not change transcript reading. n/a.

## 5. Edges

- **B2 (blocking) — the D2 acceptance rule contradicts itself, and the new words break FR-41.** Trace: `stalled=None, looped=None`.
  - Old gate: `bool(None) or (None is not False)` → True. Old `why`: "whether the story looped is not known" (:530-532). Old pack
    word: `(False, False)` → "possibly looping" (:1129-1130).
  - New: `loop_state` → (UNKNOWN, UNKNOWN). `stall != NO` → True. `_WHY[(True, UNKNOWN)]` = "the story is stalled", and
    `_STATE_WORDS[(True, "unknown")]` = "stalled".
  - So the gate is True before and after, but the text changed. D2 says "Every delta is old gate False → new gate True", so this
    row fails D2 as written. The same happens for `stalled` missing, 0 or `"x"` with looped None or True (e.g. `stalled=0,
    looped=True`: old "the story looped", new "the story is stalled and looped").
  - The new text also reports an unknown stall as a fact (FR-41). The packer's own docstring says `stalled` None is the unknown
    (`collect_pack.py:26`).
  - Fix: give UNKNOWN-stall rows their own words, e.g. "whether the story stalled is not known" (B-section text, FR-6). Or key the
    words on `stall == YES` and add the then-reachable `(False, NO)` key. Then restate D2: rows with `stalled ∈ {True, False}` are
    identical; every gate delta is False → True; every word delta is on a row with `stalled ∉ {True, False}`, and the script lists
    them.
- **Temporal, intake re-run (A4).** A story laid out from an older archive, re-collected by the new packer with a non-empty
  `ignored`, gets new lines. Its `csha` changes (`collect_intake.py:586`; the index compares at :728, :810, :826), so it reappears
  as changed once. The spec states only the old-archive and the empty-list worlds. Add this third row: expected, one time, no
  action.
- **Temporal, older driver (F-7):** see A9.
- **Positional (N1):** stated with invariants. The stop row sits inside the dedup block after `save_state()` and before
  `no_move` (:363-365 / :404). The round row sits after :405-406 and before the conductor. Correct. The refusal-cause branch
  returns at :412, after the append, so one insertion point covers both causes. Say so explicitly (A11).
- **Limits:** none added. `WINDOW_ROUND_CAP` AT/BEYOND is already the existing case (`test_story_run_loop_b_loop.py:577-587`). Fine.

## 6. Judgment (P27/AR-29)

The code names facts. L2 matches a recorded literal outcome against a data list, and `loop_state` classifies literals (`is
True`/`is False`). Neither judges meaning. Census: no new raise site, so no unit (`judgment-census.json` units come from raise
sites). `collect_stall.py::judge` stays shape/data. The rows in §1 are right. No objection.

## 7. §6 axis enumeration

All 36 axes of the current map (`docs/SIBLING_MAP.md:24-606`) are addressed. Gaps:

- **Form:** "axes 7, 8, 9, 10, 11: n/a" and "axes 19-28: n/a" are lumped. Rule 10(b) asks for one line per axis per mechanism (or
  lines that close each mechanism by name). Most lines do not name M1/M2/M3. The builders copy this block into their commit
  messages, so expand it (A7).
- **Axis 6 (measurement tools), M1: missing.** `experiments/measurers/` reads `driver-runs.jsonl`. `report_run.journal`
  (`experiments/measurers/report_run.py:142-158`) has no kind filter and counts every non-conductor row as a "role first work"
  call. `launched`, `gate_repair` and `process` rows already inflate it, and `window_round` adds more. `compare.driver_report`
  buckets by kind (harmless). Line: "axis 6, M1: queued: `report_run.journal` counts every non-conductor row as a call
  (pre-existing; candidate finding)".
- **Axis 14, M1: wrong.** "transcript selection is unchanged" is false for M1 (§2 above).
- **Axis 5 / the journal-kind data twin, M1: missing.** `driver-journal-kinds.json` (B1).

## 8. Owns and order (§4)

- **N1 ∥ N2 ∥ N3:** disjoint, with one exception. `collect_stall.py` is shared between N1 (docstring :61-78) and N2 (functions);
  the hunks are disjoint and merge cleanly. `collect_pack.py` is shared between N2 (`_pack_transcripts`) and N4 (`_stories`,
  `_stall`), and N4 runs after N2 anyway.
- **N1 vs FV1-6 in `driver_machine.py`:** disjoint. `window_round_gate` is :319, against `seam_rework_step` :578,
  `take_seam_answer` :2335 and `seam_chosen` :2388. FV1-6's batch (`live-run-fvf/batch-1`) is `ожидает` and lists the whole
  `scripts/driver_machine.py` in its row (:39).
- **The CL4 batch row's zone is stale.** `batch-4-cl3-9-ochered.md:25` "Пишет в" names `scripts/story_run.py` (the finding's stale
  writer) and `scripts/collect_intake.py` (wrong path). It does not name `driver_machine.py`, `references/collect-loops.json`,
  `tools/collect_intake.py`, `SKILL.md`, `changelog.d/…` or the tests. `piles.py check` (б) compares zones from these rows, so the
  overlap with FV1-6 in `driver_machine.py` will not be seen. The batch is not taken, so it is not frozen: the Lead updates the row
  before `take` (A8).
- **N2 owns misses `_l_state`.** Step 5 creates it (and §5a names it), but the owns list does not. The nesting DoD says "the five
  functions", and there are six (A3).
- **N4 witness:** named. `python -m pytest tools/test_collect_intake.py -q` is the test file that judges the forge paths, plus
  `scenario_walk --witness-for collect_pack.py`. Correct per rule 4.
- **N3 order:** the changelog fragment describes N1's and N4's behaviour. Merged first, it can ship text for a change that is later
  rejected. Merge N3 last, after N1 and N4 are accepted, or have the Lead edit it at the end (A5).

## 9. Executable by a weaker model?

Mostly yes: file, function, edges and test rows are named, and the direction is chosen. The holes:

- B1: N1 says to grep the readers and "fix none". The money reader must be fixed in this node, so the instruction is wrong.
- B2: the builder will hit D2 failures the spec calls impossible.
- **D2's "the pack word, old vs new" does not say how to get the OLD word.** The expression is inline in a method. A weak model
  will retype it, which tests a transcription and not the code. Spell it out: call the old and the new
  `collect_pack.Packer._pack_transcripts` on a stub `self` (`gap` captures; `_host_subagents` → `[]`; patch
  `collect_stall.session_transcripts` → `[]`), so `got` is empty and the gap text carries the state word (A1).
- `_l_state` owns gap (A3).
- `collect_pack.py:1116` unrouted (A2).

## 10. Rule-18/19 standing questions (plan gate)

- **DUPLICATION AND CONSISTENCY:** the plan collapses three readings of the pair into one (`loop_state`), but leaves a fourth at
  `collect_pack.py:1116` (A2). `_WHY` and `_STATE_WORDS` stay two sentence tables on purpose (F-2 A, bytes pinned by quarantined
  tests). That is acceptable. What I searched: `looped|"stalled"|get(.stalled.)`, case-insensitive, in `collect_pack.py`,
  `collect_intake.py`, `collect_stall.py`, plus `-l` over `tools/`, `scripts/` and `skills/`.
- **CODE QUALITY:** the `_l_records` split with ≤ 3 block levels per function is fine. W1-W3, W6 and W7 are per-edge receipts that
  `docs/TESTING.md:55-57` and the "Квитанция на ключ" row (`:94`) list as not written. Keep W4 (the join, the defect row), W5 (the
  K3/`_open_calls` invariant a real reader depends on) and the B1 price row. Fold W1-W3 into one shape check, or drop them (A10,
  the Lead's call).
- **ONE ROAD (P31):** this plan creates no exclusion. The residual second road for the pair is `collect_pack.py:1116`; fix it in
  this round (A2), not as a passed-on line.

---

## Blockers

**B1 — §3 N1 (owns, What to change, Edges "Row keys", builder check (a)): a `window_round` row makes the task price `incomplete`
(money, P18).**

- The row deliberately has no `session_id` (spec edge "Row keys"). `task_price._rows_without_session` (`task_price.py:573-585`)
  skips only kinds in `no_call_kinds` and counts every other sessionless row.
- `_no_call_kinds()` on read-main returns `['delivery', 'gate_repair', 'launched', 'note', 'rows_given_up', 'stopped_by_person',
  'trace_failed']`: `'window_round' in k` → False (run below).
- The keep table pins the effect: `test_task_price.py` KIND_CASES, "an unknown kind without a session still counts" →
  `"incomplete", 1`.
- So every story that had one S5 window round would price `incomplete`. This is the t-363 B2 class, which `task_price.py:564-566`
  describes for `launched` rows.
- Change:
  - Add `references/driver-journal-kinds.json` and `scripts/tests/test_task_price.py` (KIND_CASES only) to N1's owns.
  - Append `"window_round"` to `no_call_kinds` with a `why` ("round bookkeeping of an S5 window: no session, no money; the
    conductor call it precedes is journalled by its own row").
  - Add `"window_round"` to the `for _kind in (...)` tuple at `test_task_price.py:~1062`. That is the defect row, and it fails
    before the fix.
  - Fix builder check (a): add `task_price` and `run_counters` to the list, and replace "fix none of them" with "fix the
    no-session data row in this node; report every other reader found".
  - Add a §0 fact for the table, and add axis 5 / AR-1 lines.
  - **Sweep of the same artifact:** the `process` rows already on main (P1-v) have the same defect today. `'process' in
    _no_call_kinds()` → False, and `driver_journal.py:453-455` claims "every reader that binds sessions, prices … passes them by",
    which `task_price` does not. Either fold `"process"` into the same N1 edit (one word plus one tuple entry, same reader), or
    open a finding in P1-v's pile. This is the Lead's call. My recommendation: fold it in, since it is the same artifact and the
    same test row.

**B2 — §3 N2 (What to change 3-4, Edges row 3, Mechanical layer D2): an unknown stall is worded "stalled" (FR-41), and D2's
acceptance cannot pass.** The trace is in §5 above. Change:

- Add UNKNOWN-stall keys to `_WHY` and `_STATE_WORDS` with words that say the stall is not known. Proposed: "whether the story
  stalled is not known" / "possibly stalled". The text goes through `human-questions.md` (FR-6, section B applies to N2's FR
  pass).
- Restate the D2 acceptance as in §5.
- Fix the edge row "`stalled` = None, missing, 0, 1, `"x"` → worded as stalled" accordingly.

## Amendments (non-blocking, apply before dispatch)

- **A1 — §3 N2 Mechanical layer D2:** say how the old and new pack words are obtained (stub `self` on both `_pack_transcripts`;
  see §9). Name the old copy's import path: the scratch folder first on `sys.path`, the package `scripts/` after it.
- **A2 — §3 N4 What to change + DoD AR-13:** route `collect_pack._stall:1116` through `loop_state`. Keep the condition "looped
  unknown and not stalled": `loop == UNKNOWN and stall != YES` keeps today's bytes for `stalled` None. Extend the AR-13 grep to
  `\["looped"\]|get\("looped"|get\("stalled"\)`.
- **A3 — §3 N2 owns + DoD:** add `_l_state` to owns. Change "the five functions" to six (`_l_records`, `_l_rows`, `_l_state`,
  `_l_series`, `_l_records_flat`, `_l_nested`).
- **A4 — §3 N4 Edges:** add the third temporal row: an older-archive story re-collected with non-empty lists changes `csha` once
  and is shown as changed. Expected, no action.
- **A5 — §4:** N3's fragment merges after N1 and N4 are accepted, or the Lead edits it last. Add to the fragment one clause saying
  that a story whose window hit its cap now sends its transcripts (owner's word 30.10), and a B-id when the integrator issues one.
- **A6 — §2.4 / §6 axis 14 / N4 builder checks:** name that M1 widens which stories' transcripts leave the project (covered by the
  owner's 30.10 word, pointer). State that `ignored`/`loop_ignored` carry only the `where` strings of the existing signal
  f-strings. Add an N4 builder check: does the manifest's story item pass any redaction? Report the answer; fix nothing.
- **A7 — §6:** one line per axis per mechanism (expand 7-11 and 19-28; name M1/M2/M3 on each line). Add axis 6 (M1, queued
  `report_run.journal`), correct axis 14 (M1), and add the `driver-journal-kinds.json` twin (B1).
- **A8 — batch file `plans/piles/collect/batch-4-cl3-9-ochered.md:25`:** before `take`, rewrite "Пишет в" to the real zone:
  `driver_machine.py (window_round_gate)`, `references/collect-loops.json`, `references/driver-journal-kinds.json`,
  `scripts/collect_stall.py`, `scripts/collect_pack.py`, `tools/collect_intake.py`, `kb/04-onboarding-doctor.xhtml`,
  `skills/qa-collect/SKILL.md`, `changelog.d/collect-4-cl4-1.md` and the named tests. Drop `story_run.py`. This lets
  `piles.py check` (б) see the FV1-6 overlap, which D-0048's function lists then clear.
- **A9 — §3 N1 step 3 + F-7:** correct the docstring text. "L1/L5/L7" becomes "L1/L5", and "cannot be told" becomes "the version
  that first writes the row is not known when the row is written, so a story's version is not read". Keep F-7(a), but have the
  collector say the blind spot out loud (FR-41) in ONE H gap line per collect, not per story and not a reason, so nothing more is
  packed. Or record explicitly that the docstring "Known gap" is the only carrier. The Lead chooses.
- **A10 — §3 N1/N4 test rows:** trim W1-W3, W6 and W7 (per-edge receipts, `docs/TESTING.md:55-57`, `:94`) to at most one shape
  check. Keep W4, W5 and the B1 price row. Add one intake row for a non-string `where`/`why` (None, 3), rendered by `%s` with no
  crash: outside data, P16 one parameterised list.
- **A11 — §3 N1 What to change:** restate the line numbers on e4ba384 (§1 table). Add: the round row goes right after :406 and
  before the cause branch at :408, so both causes are covered by one insertion.

## Who applies

Every blocker and amendment is a local spec edit: lines, owns, one data row, word keys, an acceptance sentence. None changes the
design or reopens a fork, so the Lead applies them without the designer. Under PROJECT.md "новая идея" step 6, a second critic
pass is needed only if the fixes change the architecture. These do not, so the Lead checks the fixes. Exception: if the Lead picks
the A9 gap-line option, that is a new person-facing text, and it goes through FR-6 inside N2/N4's FR pass. It does not need
another plan critic.

## Fork table

| Fork | Designer rec. | Critic | Whose decision |
|---|---|---|---|
| F-1 outcome words | (a) series' own `to_conductor/same_set/cap` | **agree**: one vocabulary; `continue` does not exist (`driver_machine.py:361, :405`) | Lead (technical) |
| F-2 one mapping | (A) one classifier, sentences per site | **agree, with B2**: the UNKNOWN-stall words must not claim "stalled" | Lead |
| F-3 which ignored lists travel | (a) both | **agree**: no new content class (`where` f-strings already travel in signals). It adds fields to what leaves a project, but within the class the owner already sees | Lead; highlight it as «решила сама» in the report to the owner (data leaving projects) |
| F-4 proving the refactors | (a) one-off differential, not committed | **agree** (TESTING.md bans "like before" tests; quarantine is untouched) | Lead. (b) would be the **owner's** (against builder-rules 7b) |
| F-5 gate on `loop_state` | (a) yes | **agree**: P31; the delta is hand-made verdicts packing | Lead |
| F-6 SKILL.md:4 | (a) fix in N3 | **agree**: verified the twin of KB :408; no other "stalled"-only text in `skills/`, `references/`, `kb/` (case-insensitive grep) | Lead |
| F-7 older-driver stories | (a) no rows = no signal | **agree with A9**: say the blind spot without packing. (b) would pack transcripts of every older story on every collect (a reason is not windowed by the mark), which is more content out of every project | Lead for (a)/(a+gap line); **owner** if (b) is chosen (what leaves projects) |
| F-8 where test rows go | (a) existing functions | **agree, trimmed per A10** | Lead |
| Q-1 real archives | — | only the owner knows the inbox path (`QA_COLLECT_INBOX`) | **owner** (question, non-blocking) |
| (new) `process` kind in `no_call_kinds` (B1 sweep) | — | fold into N1 | Lead (technical; a money defect already on main, so tell the owner the same turn) |

## Trail

Read: the spec whole (540 lines); `plans/piles/collect/batch-4-cl3-9-ochered.md` whole; the `collect/README.md` CL4-1 rows (:29,
:88); `release-next/findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md:1-9`; on read-main
`collect_stall.py:1-230, 320-569, 725-788`; `collect_pack.py:1050-1144`; `driver_machine.py:300-419`; `driver_runner.py:404-420`;
`driver_journal.py:343-399, 450-459, 552-589`; `task_price.py:548-597`; `references/collect-loops.json`;
`references/driver-journal-kinds.json`; `references/run-record.json` (keys); `test_story_run_loop_b_loop.py:40-99, 499-788`;
`test_probe_gap_door.py:268-297`; `test_no_move_seam_k4s.py:222-251`; `test_task_price.py:1017-1065`; `tools/collect_intake.py:640-699`
(+ import grep); `test-layers.json` (section heads, :1410-1420, :6333-6342); `slow_tests.json` grep;
`experiments/measurers/compare.py:266-293`, `report_run.py:140-158`, `stage_role_table.py:205-220` (+ kind greps of 7 measurers);
`docs/SIBLING_MAP.md` axis heads and axis 6 (:159-181); `docs/TESTING.md:40-100`; `changelog.d/README.md:1-20`; the fixture
`local-1-arm-b/state/driver-state.json:238-260` and `driver-questions.jsonl:24-27`; `factory-out/state/driver-runs.jsonl:59-61`;
`live-run-fvf/batch-1-live-run-fvf.md:1-6, :39`.

Reruns:
- `git -C read-main log -1 --oneline` → `e4ba384 wave 1 integration report`; `git log --oneline f52faed..e4ba384 | wc -l` → 95.
- `diff --strip-trailing-cr <(git show f52faed:<f>) read-main/<f> | wc -l` for 17 files (the list in §1).
- `python -B -c "...import task_price as TP; k=TP._no_call_kinds(); print(sorted(k)); print('process' in k, 'window_round' in k, 'gate_repair' in k)"`
  → `['delivery', 'gate_repair', 'launched', 'note', 'rows_given_up', 'stopped_by_person', 'trace_failed']` / `False False True`.
  The positive control `gate_repair` is True.
- Grep `window_round_gate` across `scripts/` → callers `driver_machine.py:574`, `test_no_move_seam_k4s.py:240,243` (real driver),
  `test_probe_gap_door.py:301,312,323,352`, `test_probe_not_proved.py:281` (the stub, C19 confirmed), `test_silent_passes.py:623`
  (replaced by a lambda, unaffected).
- `grep -ln "_journal_paths|driver-runs.jsonl|RUNS_NAME|driver_runs" scripts/*.py` → the 17 modules in §1.

Not run: `scenario_walk.py --witness-for` (a builder's first output); the D1/D2 differential (it does not exist yet). I did not run
a full `task_price` over a fixture with a `process` row. The chain rests on the membership run above plus `task_price.py:579-584`
plus the pinned KIND_CASES row.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 spec 3 N1: a window_round row has no session_id and its kind is not in references/driver-journal-kinds.json no_call_kinds, so task_price._rows_without_session (task_price.py:573-585) counts it and every story with an S5 window round prices incomplete (money, P18); add the data row and a test_task_price KIND_CASES entry to N1 owns, fix builder check (a) (add task_price, run_counters; fix the money reader here). Same-artifact sibling: the process kind already on main is missing too.",
    "B2 spec 3 N2 steps 3-4 and D2: stalled UNKNOWN is worded 'the story is stalled' / 'stalled' (FR-41, collect_pack.py:26), and D2's rule 'every delta is old gate False to new gate True' fails on stalled=None,looped=None (gate True both, words change); add UNKNOWN-stall word keys and restate D2."
  ],
  "class_completeness": "Pair-reading class: a fourth site collect_pack.py:1116 is missing from N2/N4 and from the AR-13 grep (A2). Journal-kind class: the second closed table driver-journal-kinds.json is missed (B1), and its sibling kind process on main has the same defect (sweep of the same artifact; fold or queue). SIBLING_MAP: axis 6 (experiments/measurers/report_run.journal counts every non-conductor row as a call) missing for M1 (queue); axis 14 claim wrong for M1; axes 7-11 and 19-28 lumped, not one line per axis per mechanism (A7). Wording siblings KB:408, KB:417, SKILL.md:4: complete (case-insensitive grep of skills, references, kb).",
  "trail": {
    "read": [
      "docs/tasks/specs/20261113-cl4-1-collect-stalled-looped-spec.md",
      "read-main plans/piles/collect/batch-4-cl3-9-ochered.md",
      "read-main plans/piles/release-next/findings/20261030-sbor-transkripty-tolko-zavisshih-petli-ne-vidny.md",
      "read-main ai-packages/qa-factory/scripts/collect_stall.py:1-230,320-569,725-788",
      "read-main ai-packages/qa-factory/scripts/collect_pack.py:1050-1144",
      "read-main ai-packages/qa-factory/scripts/driver_machine.py:300-419",
      "read-main ai-packages/qa-factory/scripts/driver_runner.py:404-420",
      "read-main ai-packages/qa-factory/scripts/driver_journal.py:343-399,450-459,552-589",
      "read-main ai-packages/qa-factory/scripts/task_price.py:548-597",
      "read-main ai-packages/qa-factory/references/collect-loops.json",
      "read-main ai-packages/qa-factory/references/driver-journal-kinds.json",
      "read-main ai-packages/qa-factory/scripts/tests/test_story_run_loop_b_loop.py:40-99,499-788",
      "read-main ai-packages/qa-factory/scripts/tests/test_probe_gap_door.py:268-297",
      "read-main ai-packages/qa-factory/scripts/tests/test_no_move_seam_k4s.py:222-251",
      "read-main ai-packages/qa-factory/scripts/tests/test_task_price.py:1017-1065",
      "read-main ai-packages/qa-factory/scripts/tests/test-layers.json (section heads, 1410-1420, 6333-6342)",
      "read-main tools/collect_intake.py:640-699",
      "read-main experiments/measurers/compare.py, report_run.py, stage_role_table.py (driver-runs loops)",
      "read-main docs/SIBLING_MAP.md (axis heads, axis 6)",
      "docs/TESTING.md:40-100",
      "read-main ai-packages/qa-factory/changelog.d/README.md",
      "read-main fixtures/stories/local-1-arm-b/state/driver-state.json:238-260, driver-questions.jsonl:24-27",
      "read-main experiments/mybooks/factory-vs-free-agent/runs/factory-out/state/driver-runs.jsonl:59-61",
      "read-main plans/piles/live-run-fvf/batch-1-live-run-fvf.md:1-6,39"
    ],
    "reruns": [
      {"command": "git -C read-main log -1 --oneline; git log --oneline f52faed..e4ba384 | wc -l", "result": "e4ba384 wave 1 integration report; 95"},
      {"command": "python -B -c (import task_price as TP; print sorted TP._no_call_kinds() and membership of process, window_round, gate_repair)", "result": "['delivery','gate_repair','launched','note','rows_given_up','stopped_by_person','trace_failed'] / False False True"},
      {"command": "diff --strip-trailing-cr f52faed:<file> read-main/<file> | wc -l (17 files)", "result": "collect_stall/collect_pack/collect-loops/intake/KB/TESTING unchanged; driver_machine 112, driver_runner 96, test-layers 71, loop_b_loop 4 lines changed"},
      {"command": "grep -rn window_round_gate read-main/ai-packages/qa-factory/scripts", "result": "driver_machine.py:574; test_no_move_seam_k4s.py:240,243; test_probe_gap_door.py:301,312,323,352; test_probe_not_proved.py:281; test_silent_passes.py:623"},
      {"command": "grep -in 'looped|\"stalled\"|get(.stalled.)' collect_pack.py tools/collect_intake.py (positive control: known sites 1129-1130, intake 665)", "result": "extra pair decision at collect_pack.py:1116"}
    ]
  },
  "fixes": [
    "spec 3 N1 -> owns + driver-journal-kinds.json (append window_round to no_call_kinds with why) + test_task_price.py KIND_CASES tuple entry; builder check (a) add task_price, run_counters and fix the money reader in-node (B1); Lead decides folding the process kind",
    "spec 3 N2 steps 3-4, edges, D2 -> UNKNOWN-stall word keys that do not say stalled; D2 acceptance restated (B2)",
    "spec 3 N2 D2 -> old/new pack word obtained by calling both _pack_transcripts on a stub self (A1)",
    "spec 3 N4 + DoD -> route collect_pack._stall:1116 through loop_state; widen the AR-13 grep (A2)",
    "spec 3 N2 owns/DoD -> add _l_state; six functions (A3)",
    "spec 3 N4 edges -> third temporal row: csha changes once for a re-collected story with new lists (A4)",
    "spec 4 -> N3 fragment merged last; fragment names wider transcript packing (A5)",
    "spec 2.4 / 6 axis 14 / N4 checks -> name widened transcript set (owner 30.10), the where-string content class, redaction check (A6)",
    "spec 6 -> one line per axis per mechanism; axis 6 M1 queued report_run.journal; axis 14 corrected; journal-kinds twin (A7)",
    "batch-4-cl3-9-ochered.md:25 -> real write zone before take (A8)",
    "spec 3 N1 step 3, F-7 -> L1/L5 not L1/L5/L7; correct 'cannot be told'; say the blind spot once per collect or record the docstring as sole carrier (A9)",
    "spec 3 N1/N4 test rows -> trim W1-W3, W6, W7; add a non-string where/why intake row (A10)",
    "spec 0 / 3 N1 -> restate driver_machine/driver_runner/test-layers line numbers on e4ba384; one insertion after :406 covers both causes (A11)"
  ]
}
```
