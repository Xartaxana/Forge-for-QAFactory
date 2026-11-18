# t-1389 code review: PC4-10 integrator (t-1380), RD1-38 S1 (t-1385), FG7-56/61 (t-1387), FG7-3 (t-1388)

**Verdict per node**
- **PC4-10 integrator (f9fc7dbf): NEEDS WORK.** 1 blocking finding (B1), 1 fix before merge (F1).
- **RD1-38 S1 (7a9ec3f2): ACCEPT.** No blocking findings.
- **FG7-56/61 (806f0cef): ACCEPT.** No blocking findings. One residual (R2) for the Lead to file.
- **FG7-3 (9e8d36cf): NEEDS WORK.** 1 blocking finding (B2). One class sibling (R3) for the Lead to decide.

Overall JSON verdict: `blocker`, because B1 and B2 block. Each is a commit-message fix with no code change. Accepting the work stays with the Lead (rule 6).

## Findings

**B1 (blocks merge). PC4-10: three commits edit a quarantined file without the K5 door.** `ai-packages/qa-factory/scripts/tests/test_current_audit_contract.py` is in the `quarantine` section of `test-layers.json`. Commits 221fc690, 18733632 and 3b17eff3 each change it. None of their messages has `quarantine-edit: test_current_audit_contract.py -- <reason>`. `check_history` (tools/test_quarantine.py:1672, the loop at :1694-1698) flags each of those commits. So the nightly `quarantine-check` goes red on the merge. Scratch proof: `k5probe.py` is a read-only copy of that loop over the tool's own `_blob_sections`, `_touch` and `_DOORS`. It prints the refusal for all three commits. Its positive control is 1bb7a050, which touches only test-layers.json and prints nothing. Verbatim output is in the Trail. The fix is one later commit with three `quarantine-accept: <sha> -- <reason>` lines (the door at :1520, read at :1730). A reason that holds: "the pins followed the split: the TEST_TIMEOUTS rows are gone (selftest.py:143 holds only s7_live)". The other fix is to reword the three commits. The edit itself is right: the carrier selftest.py TEST_TIMEOUTS has no row for test_infra_failure.py or test_no_move_seam.py (I grepped HEAD and origin/main), so 300 is the true pin. Q5(g) class.

**B2 (blocks merge). FG7-3: the same class. Commit 9e8d36cf edits the quarantined `test_acceptance_semantics.py` without a door.** The `HANDED_ROW` import is at :602. The same probe on 9e8d36cf prints `quarantined file test_acceptance_semantics.py was changed ... expected a line 'quarantine-edit: test_acceptance_semantics.py -- <reason>'`. Fix: a `quarantine-accept: 9e8d36cf -- <reason>` commit. The other choice is to leave the quarantined copy as it was: it leaves the canon with its cohort, so the "literal lives once" key would count only the kept files. That choice is the Lead's. The other edited test files are keep rows: test_proof_level and test_window_record are `gate_named`, and test_story_run_loop_b_loop is `detector`. story_step_common.py has no row, so no door is needed for any of them.

**F1 (fix before merge). PC4-10: three keep rows in test-layers.json still say the old file imports them.** These are the `why` texts of `test_controller_release.py` (:953), `test_s5_process.py` (:5077) and `test_ticket_adapter.py` (:7428): "held by import: test_words_doors.py imports it". The shim test_words_doors.py now imports only `words_doors_common` and `harness`. The imports moved: `test_words_doors_controller.py` imports test_controller_release (:486), test_s5_process (:103 and others) and test_ticket_adapter (:628), and `test_words_doors_flight_launcher.py` and `words_doors_common.py` import test_s5_process. No reader acts on `why` (K5 reads `named_by` and the shim `why` only, :1666), so this does not block. But it is a registry text that lies, and it is on the dispatch's edge list ("every old test file name still named by a carrier"). Re-point it to the parts. A hand edit of `why` is outside split-keep, the only writer in AR-14. The integrator already hand-edited `named_by` in 221fc690, so the Lead decides whether that is acceptable.

**R1 (residual, Lead).** The probe's anchor in `driver_golden.py:906` searches `story_run.py` for `def resume_with(`. The function is at `driver_dispatch.py:2308`, so the probe refuses on main already. I confirmed this with Grep. The integrator re-pointed `file_name` to `test_story_run_refusals_resume.py`, which is correct, and reported the anchor. It needs a node with an id and an owner. The Lead opens it (Q4(d)).

**R2 (residual, Lead). FG7-56: the inline "transcripts off" collapse class (F9) has no carrier.** The SIBLING_MAP row added in 806f0cef calls it "a queued finding" but names no findings file and no node id. I searched plans/piles for "transcripts off" and found only the FG7-74 row, which is another class. A queue line without a carrier is the Q4(d) case: open a node or name its findings file.

**R3 (class sibling, Lead). FG7-3: `stand_gaps.annotate_override` (stand_gaps.py:1092-1104) is a fourth stamp loop of the same class.** It re-reads pipeline.json, adds `fields` to the live `stage_overrides` entry with `override.update(fields)`, and writes the file again. That makes it a second writer next to `record_stage_overrides(fields=)`, the one override road under AR-14 that this node's siblings line names. Its docstring says "waiver.py has no flag for an extra field", which has been false since GW1-40 added `fields=`. Callers are stand_gaps.py:1135 and :1198. It is outside this node's owns and not named in the finding (I checked the finding text). The Lead either widens the round or opens a node (Q4).

## Per-node questions

### 1. PC4-10 integrator
- **Old names in carriers:** `git grep` over HEAD (case-insensitive; excluding docs/tasks, plans/piles and logs) for the three old names. What remains:
  - The shims themselves.
  - Parts' docstrings ("a part of X").
  - `covers` entries in the importers' rows. These are true: the importers import the shim.
  - The importers: test_exit_ask_tools, test_s6_reprove_manual, test_story_run_deferred, test_story_run_s0, test_detector_verdict and test_story_run_repair_limit. Every name they import is re-exported by a shim. I checked each `WD.` and `WORDS.` attribute against the shim's `__all__`.
  - plans/features.json:498, which names the shim (still on disk).
  - CHANGELOG history, and plans/BACKLOG.md and MEASUREMENTS.md history. These are non-goals.
  - Prose in test docstrings outside owns: test_story_run_gate_repair.py:19, test_story_run_s7.py:4, test_story_step_manual_block.py:11, test_s6_reprove_manual.py:4 and :144. Not blocking; the Lead can sweep them in a later round.
  - F1.

  These carriers name no old file any more: gate-registry, driver-layers, driver-golden-rules, mutations fixture, state-exits, slow_tests, TEST_TIMEOUTS, lint-baseline, test_conductor_doors, test_silent_passes, architecture.md and SIBLING_MAP:146. I read the diff.
- **Nothing lost:** `splitcmp.py` (AST, old blob at the merge base against the common module plus the parts at HEAD) found:
  - s6: 57 defs, 0 missing, 0 changed bodies, 0 main() calls lost, 298 = 298 check calls.
  - refusals: 59 defs, 0 missing, 0 changed, 0 calls lost, 659 = 659.
  - words_doors: 75 defs, 0 missing, 0 changed, 0 calls lost, 342 = 342.

  The shims run nothing without `--all`.
- **Registries:** the stand_login_gate pointer goes to t292, which holds the direct `driver.stand_login_gate(plan)` call (:282) and the K15 case. c16b holds only the price text, so t292 is right (t-1376 B1 class). The keep-split commits 1bb7a050, eed60499 and d47438f2 each carry the door line. The tool's own `_split_problems` finds no problem in any of the three (k5split, Trail). 4 parts are over 60 s provisional (manual 103.9, flight_launcher 79.6, t292 75.8, core 61.5). They are named in the report and not re-split, which matches the edge.
- **Audit-contract pin:** I read it from the carrier. HEAD selftest.py has only `test_story_run_s7_live.py: 600` among the names pinned, and origin/main is the same. So 300 for infra_failure and no_move_seam is right. Main's version of the file pins 600, so it is red on main today, and this branch fixes that.
- **Inherited `layer`/`why`/`named_by` on the five non-core refusal parts** (all "detector", named_by core:472/475): split-keep copies these by design. This is the class t-1376 already proposed as a node, so it is not a new finding.
- Merge with today's origin/main: `git merge-tree` is clean (13 commits ahead, no test carrier touched).
- Q6: none found; one road is test_split plus split-keep. Q7: no new code beyond pointers. Q9: lint-baseline was re-keyed (s6 to c16b, count 2, not raised). slow_tests and TEST_TIMEOUTS lost rows and gained none. No raise of any ratchet. Q10: AR-13, AR-14, AR-20, AR-22 and AR-24 are named in 221fc690. VARIETY: n/a, test harness only. Q11: none. Q12: none found; the one road is split-keep. Q8: Cyrillic scan of the package files in the diff is clean (positive control: test_ascii_line.py was found).

### 2. RD1-38 S1: ACCEPT
- **One reader:** `pinned_frames(` is called only at reporters.py:452, and `_pinned_read` survives only as a docstring mention (reporters.py:443). Grep over the whole tree at 7a9ec3f2, excluding docs/tasks. The control in the same Grep shape is `_LOCATION_RE`, which is still found in red_sandbox.py:786/799/1616 and is still used, so the handoff's "may be unused" note is moot.
- **Verdicts kept, red_sandbox:** traced line by line.
  - The guard (`"site_unread" in site` and failed) is the same.
  - The location parse moved from `_LOCATION_RE` to `rpartition` plus `pinned_frames`' own `[1-9][0-9]*` gate. `None`, a missing colon, `0`, `05` and `5x` still give "nothing pinned".
  - The second read uses the same grammar arguments, and `pinned_site`'s defaults (`pytest_command=True`, `runtime=""`) match the `hint={}` path.
  - The three clauses are word for word.
  - `reason_agrees(message, expected)` equals the old `reason_matches(reason, expected)`.
  - The reason text is joined the same way ("; why").
- **P8 is real:** `p8probe.py` drives the row through `assertion_site`. The second read returns `location tests/Calc.kt:5, kind assertion`. With the failure's message the result is unread with "...not the pinned one". With the error's message it would be confirmed as `tests/Calc.kt:5`. So the new row kills the "compare the second read's message" mutation.
- **P9:** `judge_probe_row` copies the site only into `observed` ("no step reads the failure's wording or place to prove"). Verdict, cause and proved_by do not depend on it, and `failure_kind` alone changes. **P10:** a pinned site is the location of a key of this run, which is in `edits`, so `_earlier_check_at` skips it.
- **Edge `record["expected_location"]`:** subscripted already at :4380 in the same function. An alternative record (:5716) holds `None`, so it is returned unchanged.
- Tests: Q5(a) the new probe_marker test fails if the `_judge_rows` call is removed (seen[0] would stay unread). Q5(b) the expected values come from card §3 S1, P7 and P8. Q5(c): the walk hook has no row of its own. Card §6 asked for only the two rows and states that the walk hook adds facts and no verdict, so this is a spec choice and not a finding. Q6, Q7, Q9, Q11 and Q12: none found (one road, `pinned_site`, for all three call sites). Q10: AR-13, AR-28 and AR-29 are named. VARIETY: no new block; an unknown pin stays unread.

### 3. FG7-56/61: ACCEPT
- **W1 bytes:** `w1probe.py` exec's each OLD function from e3f237ac and compares it with the NEW name over 18 values and every cap the members use. The values: None, "", whitespace, `\t \n \r \x00 \x1f \x7f`, non-ASCII, astral, a lone surrogate, 1000 chars, int, float, bytes, list, NEL/LS, NBSP, C1, backslashes. The caps: None, 0 and the real ones. The members: coordinator_rules, tier_echo, journal_echo x2, session_context, wait_reaper, crap_report, wiring_check. Result: 486 cases, 12 diffs. All 12 are the deliberate loss of the default cap on `coordinator_rules._ascii` and `tier_echo._ascii_sanitize` (E9/W2: "the cap is required"). Every call site passes the cap: coordinator_rules:74 passes 160 and tier_echo:215/222 pass 80. A tree-wide Grep found no outside caller of either. Those 12 diffs are also the probe's own negative control.
- **Net:** the closure of live wiring contains `ascii_line`. Dropping its MECHANISM_PREFIXES row gives `uncovered ['ascii_line']`, so the test would catch a missing row.
- **session_context without the helper:** `scprobe.py` blocks the import. Result: rc 0 and one line, `session-context warning: ModuleNotFoundError: <unprintable exception>`. Unblocked, the same run prints 94 lines. So it degrades as card F2(b) states. Note, not a finding: the warning line no longer names the module, because the failure line's own sanitizer is the missing helper.
- From another cwd: each hook runs as `python tools/<x>.py`, so sys.path[0] is tools/. enforcement_probe runs wiring_check from the working tree (:265). crap_report and wait_reaper insert their own folder into sys.path. The import of ascii_line in wiring_check is not guarded, unlike `gitcmd`'s F6-39 guard. Card F2(b) chose this ("wrapped only in session_context"), and a broken helper fails enforcement_probe closed.
- Q6: the SIBLING_MAP axis 15 row lists what is in and what is out, with reasons. Q7: no dead code (`import re` was removed from tier_echo, and journal_echo still uses `re`). Q10: AR-15. Q12: one road, R2.

### 4. FG7-3: NEEDS WORK (B2)
- **One stamp loop:** `_stamp` (waiver.py:1201-1209) is the only `update(fields)` over class fields in waiver.py. `record_stage_overrides` takes its own `fields=` road at :1376.
- **Bytes unchanged:** `stampprobe.py` compares the old revoke and remark loops with `_stamp` across classed values None, {}, "", "x", 0, a dict, a dict with unchecked, and a list of pairs. The pipelines include junk entries, None, two matching entries and a missing or None `stage_overrides`. Result: 32 cases, 0 diffs in json.dumps or exception. `pipeline["remarks"]` and `["gate_waivers"]` are now read even when classed is None. Both are created by `apply_remark` (:192) and `apply_waiver` (:130) before the call, so that cannot raise.
- **handed_row default:** it equals the old literal, `json.dumps` matches byte for byte, and each call returns a new dict. The overrides keep the key order (case, reason, detail). test_proof_level now shares `HANDED`, and `proof_required` only reads it.
- **test_waiver_release :424 is pre-existing:** confirmed by reading. On origin/main, :424 is `re.search(r'STAND_LOGIN_BLOCK\s*=\s*(\S+)', story_run.py).group(1)`. `STAND_LOGIN_BLOCK` is defined only at driver_stage_s6.py:971; the same `git grep` finds it there and nothing in story_run.py. So the search returns None and `.group` raises. The file is identical at the node's parent and at origin/main. It is quarantined, so it runs only in the `--quarantined` watch.
- Q5: no new behaviour, no test owed. Q6: R3. Q9 and Q11: none. Q10: AR-13 and AR-15 are named.

## Trail
- Read: the four handbacks (scratchpad hb-int, hb-rd138, hb-fg756, d-fg73); reports t-1380, t-1385 and t-1387 (the line on F9), and t-1388; cards RD1-37/38 (§4, §6 S1, §9 F1, Lead decisions) and FG7-56/61 (E-list, F2); review t-1376 (B1, B2 and the note at :77); tools/test_quarantine.py :1511-1530 and :1672-1731; the shims; test-layers.json rows; the diffs of every node; probe_by_code.py `_judge_rows`, `judge_probe_row` (head), `_walk_run_once`, `_walk_attempt` and `_earlier_check_at`; reporters.py :405-466; session_context.py main and coordinator_rules_lines; enforcement_probe.py :40-75 and :255-300; waiver.py `class_fields`, `apply_*` and `_stamp`; stand_gaps.py :1092-1104.
- Reruns (verbatim tails):
  - `python -B ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py` (RD1-38 worktree): `=== test_red_sandbox_reports: 379/379 ok ===`, `exit=0`
  - `python -m pytest tools/test_ascii_line.py -q` (FG7-56 worktree): `16 passed in 0.30s`
  - `python -m pytest tools/test_mechanism_gate.py -q -k transitive_import_closure`: `1 passed, 570 deselected in 1.48s`
  - `k5probe.py <int wt> 3b17eff3 18733632 221fc690 1bb7a050`: three lines `quarantined file test_current_audit_contract.py was changed ... expected a line 'quarantine-edit: test_current_audit_contract.py -- <reason>'` (3b17eff3, 18733632, 221fc690), `probe done 4`
  - `k5probe.py <fg7-3 wt> 9e8d36cf`: `9e8d36cf quarantined file test_acceptance_semantics.py was changed ...`, `probe done 1`
  - `splitcmp.py`: `test_story_run_s6.py defs old 57 missing [] body-changed [] main-calls lost [] checks old 298 new 298`; refusals `59 ... 659 new 659`; words_doors `75 ... 342 new 342`
  - `p8probe.py`: `second: {'location': 'tests/Calc.kt:5', 'failure_kind': 'assertion', ...}`; `'AssertionError: other' -> unread | ...but its message is not the pinned one`; `'AssertionError: sum must be 4' -> tests/Calc.kt:5`
  - `w1probe.py`: `cases 486 diffs 12` (all 12 `DIFF-default` on coordinator_rules._ascii and tier_echo._ascii_sanitize)
  - closure control: `ascii_line in closure: True`, `uncovered without the row: ['ascii_line']`
  - `scprobe.py block`: `session-context warning: ModuleNotFoundError: <unprintable exception>`, `rc=0`; `none`: 94 lines, exit 0
  - `stampprobe.py`: `cases 32 diffs 0`; `handed_row default == old literal: True True True`
  - `git merge-tree --write-tree HEAD origin/main` (int): clean tree 765427b0
  - `k5split.py <int wt> 1bb7a050 eed60499 d47438f2` (the tool's own `_split_problems`): `problems: none` for each of the three splits, `keep rows gone: []`. Full-range K5 emulation `k5full.py <int wt> ef2e88ed..HEAD` (finished after the hand-off; edit doors, merge edits, split doors, removed keep rows and import edges): `commits 16`. Its only refusals are the three B1 lines (221fc690, 18733632, 3b17eff3); there is no merge, split or import-edge problem.
- All probe scripts are in the scratchpad (k5probe.py, k5full.py, splitcmp.py, p8probe.py, w1probe.py, scprobe.py, stampprobe.py). They are read-only; no live or worktree file was changed.

```json
{
  "verdict": "blocker",
  "blockers": [
    "B1 PC4-10: commits 221fc690, 18733632, 3b17eff3 edit the quarantined test_current_audit_contract.py with no 'quarantine-edit: test_current_audit_contract.py -- <reason>' line; test_quarantine.py check_history (:1694-1698) flags all three (scratch k5probe output); fix: one later commit with three 'quarantine-accept: <sha> -- <reason>' lines",
    "B2 FG7-3: commit 9e8d36cf edits the quarantined test_acceptance_semantics.py (:602) with no quarantine-edit line; same K5 refusal (scratch k5probe output); fix: 'quarantine-accept: 9e8d36cf -- <reason>' or leave the quarantined copy as it was (Lead's choice)"
  ],
  "fixes": [
    "F1 PC4-10 test-layers.json :953, :5077, :7428: the why 'held by import: test_words_doors.py imports it' should name test_words_doors_controller.py (plus flight_launcher and words_doors_common for test_s5_process); not blocking",
    "R1 Lead: open a node for driver_golden.py:906 (the resume_with anchor is searched in story_run.py; the function is at driver_dispatch.py:2308)",
    "R2 Lead: give the inline transcripts-off collapse class (F9) a node or findings file; the SIBLING_MAP axis 15 row names none",
    "R3 Lead: stand_gaps.annotate_override (stand_gaps.py:1092-1104) is a fourth stamp loop and a second writer of stage_overrides beside record_stage_overrides(fields=); widen the round or open a node"
  ],
  "class_completeness": "B1 and B2 are one class (an edit to a quarantined test with no K5 door) in two nodes of this topic; no other edited file in the four diffs is quarantined (checked against test-layers.json). PC4-10: every carrier on the edge list was walked; old names remain only in shims, importers served by shim re-exports, covers of importers, history and prose (F1 is a registry text). FG7-56: SIBLING_MAP axis 15 row and MECHANISM_PREFIXES row present, closure detector proven to catch a missing row. RD1-38: SIBLING_MAP :147 names pinned_site; all three call sites take it. FG7-3: sibling stand_gaps.annotate_override (R3) is outside owns and is for the Lead.",
  "trail": {
    "read": [
      "docs/tasks/specs/reports/t-1380-pc4-10-integrate.md",
      "docs/tasks/handoffs/t-1385-rd1-38.md",
      "docs/tasks/specs/reports/t-1387-fg7-56-61.md",
      "docs/tasks/specs/reports/t-1388-fg7-3.md",
      "docs/tasks/specs/20261118-rd1-37-38-probe-site-door-card.md",
      "docs/tasks/specs/20261118-fg7-56-61-ascii-helper-card.md",
      "docs/tasks/specs/reviews/t-1376-pc4-10-n14-rd1-40-code.md",
      "tools/test_quarantine.py:1511-1530,1672-1731",
      "ai-packages/qa-factory/scripts/tests/test-layers.json (rows of the three splits and held-by-import rows)",
      "ai-packages/qa-factory/scripts/reporters.py:405-466",
      "ai-packages/qa-factory/scripts/probe_by_code.py (_judge_rows, judge_probe_row, _walk_run_once, _walk_attempt, _earlier_check_at)",
      "ai-packages/qa-factory/scripts/red_sandbox.py (reason_matches, target_result)",
      "tools/session_context.py (main, coordinator_rules_lines, N4 block)",
      "tools/enforcement_probe.py:40-75,255-300",
      "ai-packages/qa-factory/scripts/waiver.py (class_fields, apply_waiver, apply_remark, _stamp, run_*)",
      "ai-packages/qa-factory/scripts/stand_gaps.py:1092-1104"
    ],
    "reruns": [
      {"command": "python -B ai-packages/qa-factory/scripts/tests/test_red_sandbox_reports.py (RD1-38 worktree)", "result": "=== test_red_sandbox_reports: 379/379 ok === exit=0"},
      {"command": "python -m pytest tools/test_ascii_line.py -q (FG7-56 worktree)", "result": "16 passed in 0.30s"},
      {"command": "python -m pytest tools/test_mechanism_gate.py -q -k transitive_import_closure (FG7-56 worktree)", "result": "1 passed, 570 deselected"},
      {"command": "scratch k5probe.py on 3b17eff3 18733632 221fc690 1bb7a050 and on 9e8d36cf", "result": "quarantine-edit refusal on the three integrator commits and on 9e8d36cf; control 1bb7a050 silent"},
      {"command": "scratch splitcmp.py (old blob vs common+parts)", "result": "0 defs missing, 0 bodies changed, 0 main calls lost; check calls 298/659/342 equal"},
      {"command": "scratch w1probe.py (old functions vs new names)", "result": "486 cases, 12 diffs, all the deliberate default-cap removal"},
      {"command": "scratch scprobe.py with ascii_line blocked", "result": "rc=0, one warning line; unblocked 94 lines"},
      {"command": "scratch stampprobe.py", "result": "32 cases 0 diffs; handed_row default equals the old literal"},
      {"command": "scratch p8probe.py", "result": "P8 row reaches the message clause; the error's message would confirm"}
    ]
  }
}
```
