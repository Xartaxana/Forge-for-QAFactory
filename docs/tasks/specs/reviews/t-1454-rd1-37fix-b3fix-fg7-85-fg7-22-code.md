# t-1454 -- code review: RD1-37 S3 fix round, FG7-78 B3 fix round, FG7-85, FG7-22

## Verdicts, one per node (inputs to the Lead's acceptance; the decision is the Lead's, rule 6)

- **RD1-37 S3 fix** (376840f6..1fdbf8db, against t-1443 F1-F4): **NEEDS WORK**, 0 blocking. F1, F3 and F4 are fixed. F2 is fixed only in the two functions the review named; the same surface has three more refusals that print the live door on the `--product` road (R1). Fixes R1 and R2 come before merge. R3 and R4 are low.
- **FG7-78 B3 fix** (92388b3d..34bc7d2f, against F6): **ACCEPT**. F6 is fixed. The file stays `.proposed`, and the Lead moves it.
- **FG7-85** (origin/main...cd8d8ea7, base 980992e7): **NEEDS WORK**, 1 BLOCKING (P1). The new auto refresh overwrites the root's journal with the kept copy and then deletes the copy. A line written inside the window is lost, and the run still exits 0.
- **FG7-22** (origin/main...fa7b4660, base 6ed0a333): **ACCEPT**. One card-text conflict goes to the Lead (G-note).

The JSON block says `blocker` because P1 blocks. Per node: RD1-37 is fit_with_fixes, B3 is fit, FG7-85 is blocker, FG7-22 is fit.

## Findings

**P1 (FG7-85, BLOCKS).** `_auto_refresh` discards journal lines written inside the window.
- Where: `tools/wave.py:554` `_atomic_write(root / rel, copy.read_bytes())`, then `:562` `copy.unlink(missing_ok=True)`.
- The problem: the new step writes the copy over the root's journal without reading what the file holds now. `swap()` guards against exactly this (`left != expected` carries over the tail of an unlocked appender, Q5a, and `_sha(now) == _sha(target)` verifies the write), and the auto road skips both guards.
- Failure input (scratch test, the fixtures of `tools/test_wave.py` imported as they are): the branch puts `L1+L2` on main, and the root journal is `L1+L2`. In hook `step9-locked`, an unlocked writer appends `L3` (as `test_unlocked_appender_in_the_window_is_carried_over_Q5a` does), then `OSError("disk says no")` is raised.
  - FG7-85 tree: `RC 0` / `journal restore failed (disk says no); the copy equals origin/main, so the root was staged and fast-forwarded by wave` / `ROOT-JOURNAL b'{"n":1}\n{"n":2}\n'` / `COPIES []` / `L3 anywhere: False`.
  - Control, the same test on origin/main's wave.py (the root's `tools/wave.py` equals origin/main, checked by `git diff --quiet`): `RC 1` / `JOURNAL RESTORE FAILED ... copy kept at ...` / `ROOT-JOURNAL b'{"n":1}\n{"n":3}\n'` / `COPIES [b'{"n":1}\n{"n":2}\n']` / `L3 anywhere: True`.
- Why it blocks: a journal line is destroyed, and the run reports success (exit 0, copy deleted). An unknown becomes a pass (FR-41). The scenario is realistic: the OSError branch exists for WinError 5 on `os.replace` (t-1414), which means another process holds the file, and that is the moment an unlocked writer is likely to be appending.
- The same overwrite happens when the OSError comes after a successful merge (the `kept` target write fails): the tail `swap` computed is dropped.
- Fix: in `_auto_refresh`, before writing, read the current bytes. Proceed only when they equal `git show HEAD:<rel>` or the copy. Otherwise return `"the journal changed inside the window"`, so the copy and the hint stay. Alternatively, carry the tail over the way `swap` does. Add one parametrised row, `equal-but-appended`, with the scratch scenario above: rc 1, `L3` still on disk or in the copy.

**P2 (FG7-85, fix before merge, Q5(c)).** Two refusal reasons of the new door have no row.
- Missing: `auto refresh refused: the root has other staged changes` (a named edge of dispatch t-1448), and the ff-refused reason with git's text (also a named edge; the builder reported it as not written).
- Only `off_main` is a row (`tools/test_wave.py:430`).
- Fix: add `staged` (stage a foreign file in the hook) and `ff_refused` (make an overlapping unstaged foreign change) to the same `case` table. The budget allows it: +20/-7 test lines against +33 product lines.

**P3 (FG7-85, fix before merge, Q7: a text that lies).** The module docstring still describes the old behaviour.
- Where: `tools/wave.py:31-38`. It says "wave never stashes, resets, checks out or discards anything in the root" and "A mismatch keeps the copy and is exit 1".
- Why it is wrong now: the restore-failed branch now stages the journal and fast-forwards the root, and (with P1) it can discard bytes.
- The builder noticed this and left it. Fix: one sentence naming the FG7-85 branch and its two preconditions.

**R1 (RD1-37, fix before merge; class completeness of t-1443 F2, rule 5 and rule 14).** Three more refusals on the `--product` road print the live door.
- The surface is "the door text of a refusal on the `--product` road". Besides `_judge_input` and `_demand_critic_dispatch`, these still print `JUDGE_DOOR`:
  - `probe_by_code.py:7984` (`_judge_cli`, `--task`/`--dispatch` missing);
  - `:7981` (`--s6-close`);
  - `:8409` (the stray-flag refusal, which after F3 also fires for a lone `--product`).
- Proof (scratch, the worktree's `main()`):
  - `--judge I1 --product --verdict fires --quote q` gives `2 names --product door: False`;
  - `--task T-1 --dispatch D1 --test X --product` gives `2 names --product door: False`.
- Why it matters: this is F2's own risk. A critic who copies the printed door drops `--product` and judges the live record.
- Fix: in `_judge_cli`, set `door = JUDGE_PRODUCT_DOOR if args.product else JUDGE_DOOR`. In the stray refusal, print `JUDGE_PRODUCT_DOOR` when `--product` is among the stray flags. The live text stays byte for byte the same (D15).

**R2 (RD1-37, fix before merge, Q5(a)/(c)).** The product door passed to `_demand_critic_dispatch` has no row.
- Where: `test_probe_marker_judgment.py:334`. The product loop has no dispatch row, and the new assert checks the product door only for `D4` and `D5`.
- Consequence: drop `JUDGE_PRODUCT_DOOR` from the `_demand_critic_dispatch` call in `_judge_product` (`probe_by_code.py:7897`) and every test still passes.
- Fix: add a `dispatch` entry to `patches` that builds its world with `open_dispatch=False`, and include it in the product-door assert.

**R3 (RD1-37, low, Q5(c)).** The new D14 test sits at an internal boundary and does not check the full outcome.
- Where: `test_publish_failure_keeps_the_receipt_and_notes` (`:347`) calls `publish_product_refs` directly.
- It kills the defect it exists for (remove the `try` and the test raises). But it does not assert the outcome D14 states at the door: the record is `intended_failure`, the receipt stays, and the note is in the record.
- Preferred: one `fires` row through `judge_record(..., product=True)` with `RS.subprocess.run` patched. Acceptable as is if the Lead prefers.

**R4 (RD1-37, report only, rule 12).** The witness does not cover the F4 edit.
- The witness `50 passed` covers `test_probe_marker_judgment.py` alone. `test_red_sandbox_probe.py` is a harness script that pytest collects as 0 tests (`no tests collected`; the 50 tests are all in the other file). So the F4 edit was not run by the witness.
- I ran its function myself: `no_row_language_reaches_a_counted_receipt` gives `12/12 ok`, including `PASS ...and the S2 note names --judge, --product and the record path`.
- So F4 holds. The report line "whole file" should say "harness, run via its function".

**G-note (FG7-22, for the Lead, not a builder finding).** The card contradicts itself on the "superseded-retry" row.
- Card §4 says that row expects no WARN, but E13 and the §12 decision F3 (b) make the `rejected` of the unreturned attempt 1 WARN.
- The builder asserted the consistent reading: exactly one WARN, and it holds `rejected before the worker returned`, so the `accepted` is silent. This still kills an E7 regression (a still-owed `a1` would add a second WARN and the count would fail).
- This is a dispatcher-side text defect (rule 11 (2)) for calibration.

## Standing questions

**RD1-37 fix**
- **Q1:** F1 is fixed in the one road: `red_sandbox.py:1716`, the note is appended to the same `notes` list `_judge_product` writes, so D14 holds. F3 and F4 are fixed. F2 is partial (R1).
- **Q2:** the `[:500]` cap on the note is safe.
- **Q3:** additive keyword defaults; live output unchanged.
- **Q4:** see R1. `probe()` gets F1 through the shared function.
- **Q5:**
  - (a) the F1 and F3 tests kill their defects; R2 is the gap.
  - (b) the values trace to D14 and the F3 text.
  - (c) R2 and R3.
  - (d) the F4 tuple element was replaced, not dropped.
  - (e) none.
  - (f) volume on the node branch: tests +89 against product +208 (numstat 0e6b7ff8..1fdbf8db).
- **Q6:** none found. The door strings are derived (`JUDGE_PRODUCT_DOOR = JUDGE_DOOR + " --product"`).
- **Q7:** none beyond R1.
- **Q8:** not separately checked.
- **Q9:** the fix touches no ratchet (numstat lists no fixture).
- **Q10:** unchanged from t-1443.
- **Q11:** adds no judgment.
- **Q12:** none found (no language or runner names in the fix diff).

**B3 fix**
- **Q1:** job-level `defaults.run.shell: bash` covers both `| tee` steps. `yaml.safe_load` gives `{'run': {'shell': 'bash'}}`, and no step overrides `shell`. The builder's step-body run plus its control reproduce F6's semantics.
- **Q2/Q3:** no other change.
- **Q4:** a class-note correction. t-1443 said "no sibling workflow uses tee", but `scenario-clock.yml:97` pipes into `tee` with no shell. That step is `if: always()` plus `continue-on-error: true` (a report print), so its exit is no gate. It is not an F6 instance, so nothing needs fixing.
- **Q5:** the DOC-DISPATCH witness has its keys, full source and a negative control.
- **Q6-Q12:** none found.

**FG7-85**
- **Q1:**
  - equal copy: auto refresh, exit 0, one line (row `equal`);
  - differing copy: exit 1, no clause (row `differs`);
  - off main: refused, hint plus reason (row `off_main`);
  - other staged changes and ff refused: implemented, but with no rows (P2).
  - P1 breaks the unstated invariant of the restore branch: no journal byte is lost.
- **Q2:** `_atomic_write` before `git add` is acceptable. `staged.split()` splits a path with spaces, which leans toward refusing, so it is safe.
- **Q3:** additive; the hint and the byte-level MISMATCH branches are untouched.
- **Q4:** sibling `wave.py:499`. Its ff runs under `swap`'s carry-over and verification, and the new ff at `:557` has neither (P1).
- **Q5:**
  - (a) P1 has no row;
  - (b) the asserted phrase "staged and fast-forwarded by wave" is the builder's own; the spec named no text (against the spec, does not block);
  - (c) P2;
  - (d) the renamed test still holds the old rows (`equal`/`differs` replace True/False);
  - (e)-(g) none.
- **Q6:** the on-main read at `:549` repeats `:457`; both are inline git calls with no helper. Not a second implementation of a shared helper.
- **Q7:** P3. `_auto_refresh` is about 20 lines with nesting of 2.
- **Q9:** none touched.
- **Q10:** the package AR map does not cover forge `tools/wave.py`: a grep for `wave.py` in `design/architecture.md` found 0. VARIETY: n/a (a forge tool).
- **Q11:** none.
- **Q12:** none found (no language, runner or project branch).

**FG7-22**
- **Q1:**
  - 2.1: the walk, `owed` and its replacement, `replaces_worker`, stripped refs, the date gate on the delegated line, judging only new lines (`pos >= new_from`).
  - 2.2: the text matches verbatim.
  - 2.3: wiring, plus docstring item 21 and matrix item (c).
  - The tag equals `matrix_warnings`'s (`len(head)+idx+1`).
  - Acceptance 2 (a def and one call) holds by my grep.
  - E12: a guarded parse plus try/except.
  - E16: order decides.
- **Q2:** both deviations are consistent (the G-note, and the `other-returned` row avoiding a 9f FAIL).
- **Q3:** additive; `decide()` and FAIL are unchanged.
- **Q4:** siblings checked.
  - `matrix_warnings` is the one channel; its callers are `journal_validator.py:1558/2028/2455` and `journal_write.py:612`.
  - `journal_echo` is not among them (the card's 2.4).
  - Nothing outside the validator parses these WARN texts (grep `INDEPENDENT CONTEXT|before the worker returned` in tools outside tests found only `journal_validator.py`).
  - Field semantics, measured on the live journal (rule 13):
    - `returned` refs have the same `agent:<id>` form as the delegated refs (`dev1.jsonl:2162`);
    - `replaces_worker:agent:<id>` matches the ref form (5 lines);
    - of 104 WARNs: 99 owed refs have no `returned` anywhere, 4 have it after the verdict (the t-057 class), and 1 is a resumed ref under a new task id (the E3 class, filed as FG7-88).
- **Q5:** (a)-(c) 9 rows through `decide_with_warnings`, values from 2.2/E1-E13; the volume is +55 against +60; (d)-(g) none.
- **Q6:** a second walk next to `matrix_warnings`'s, as card 2.3 prescribes. Not a finding.
- **Q7:** none blocking. `len(list(seed_lines))` is recomputed per WARN at the tag (a cosmetic cost).
- **Q9/Q11:** none.
- **Q10:** the commit names AR-13/AR-22. VARIETY: n/a.
- **Q12:** none found.

## Trail
- Read:
  - the t-1443 review in full; card FG7-22 §2-§4 and §7-§12; pile rows FG7-22 (:47), FG7-85 (:110), FG7-88 (:113); the four handoffs;
  - the fix and node diffs above;
  - `probe_by_code.py:7863-7960`, `7972-7992`, `8400-8412`; `red_sandbox.py:1654-1722`;
  - `test_probe_marker_judgment.py:290-370`; `test_red_sandbox_probe.py:1099-1121`;
  - `wave.py:25-40`, `455-575`; `test_wave.py:405-455`;
  - `journal_validator.py:382-391`, `745-835` and its call sites;
  - `journal_write.py:600-616`; `docs/TESTING.md:213-235`; `driver-golden.yml.proposed`; `scenario-clock.yml:80-104`.
- Reruns (verbatim tails):
  - RD1-37 `pytest test_probe_marker_judgment.py -k "publish_failure or stray_flag or refusals_name_the_door"` gives `3 passed, 47 deselected in 2.28s`;
  - `pytest test_red_sandbox_probe.py --collect-only` gives `no tests collected`;
  - the harness function gives `=== rs-probe-one: 12/12 ok ===`;
  - scratch `main()` gives the R1 lines;
  - FG7-85 `pytest tools/test_wave.py -k restore_oserror` gives `3 passed, 124 deselected in 17.00s`;
  - the scratch P1 test on the FG7-85 tree and on main gives the quoted lines;
  - FG7-22 `pytest tools/test_journal_validator.py -k verdict_before_returned` gives `9 passed, 319 deselected in 0.58s`;
  - the live-journal probe gives `warns 104` with the classes above;
  - B3 `yaml.safe_load` gives `{'run': {'shell': 'bash'}}`.

```json
{
  "verdict": "blocker",
  "blockers": [
    "P1 (FG7-85): tools/wave.py:554 _auto_refresh writes the kept copy over the root journal without reading it and :562 deletes the copy; a line an unlocked writer appended inside the window is lost with exit 0 (scratch: RC 0, ROOT-JOURNAL L1+L2, COPIES [], L3 anywhere False; on main the same input gives RC 1 and L3 kept)"
  ],
  "fixes": [
    "P1 (FG7-85, blocks): before writing, require the current journal bytes to equal HEAD:<rel> or the copy, else refuse 'the journal changed inside the window' (copy and hint stay), or carry the tail as swap does; add row equal-but-appended",
    "P2 (FG7-85): add staged and ff_refused rows to test_restore_oserror_in_the_window_names_the_copy_Q5c (tools/test_wave.py:430)",
    "P3 (FG7-85): tools/wave.py:31-38 module docstring - name the FG7-85 auto refresh branch and its preconditions",
    "R1 (RD1-37): probe_by_code.py:7981, :7984 and :8409 print JUDGE_DOOR on the --product road; use JUDGE_PRODUCT_DOOR when args.product (stray refusal: when --product is stray)",
    "R2 (RD1-37): test_probe_marker_judgment.py:334 - add a product dispatch row (open_dispatch=False) asserting JUDGE_PRODUCT_DOOR",
    "R3 (RD1-37, low): express the D14 test through judge_record(product=True, fires) asserting intended_failure, receipt kept, note in the record",
    "R4 (RD1-37, report): the witness covers test_probe_marker_judgment.py only; test_red_sandbox_probe.py is a harness (0 collected); F4 verified by the critic's run 12/12"
  ],
  "class_completeness": "RD1-37: F1 fixed in the one road publish_product_refs (probe() covered); F2 class walked on the surface 'door text of a --product refusal': three sites left (R1). B3: the only other tee pipe, scenario-clock.yml:97, is continue-on-error and is no gate, so not an instance. FG7-85: sibling wave.py:499 ff runs under swap's carry-over and verify, which the new ff at :557 lacks (P1). FG7-22: matrix_warnings is the one channel (callers journal_validator 1558/2028/2455, journal_write 612); journal_echo is not reached; no outside reader parses the WARN text.",
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1443-rd1-37s3-fg7-78b2b3-code.md",
      "docs/tasks/specs/20261118-fg7-22-accept-before-last-worker-line-card.md sections 2-4, 7-12",
      "plans/piles/forge/batch-7-vhodyashchie-4.md rows FG7-22, FG7-85, FG7-88",
      "handoffs t-1445, t-1446, t-1448, t-1444",
      "probe_by_code.py 7863-7992, 8400-8412; red_sandbox.py 1654-1722; test_probe_marker_judgment.py 290-370; test_red_sandbox_probe.py 1099-1121",
      "tools/wave.py 25-40, 455-575; tools/test_wave.py 405-455",
      "tools/journal_validator.py 382-391, 745-835 and call sites; tools/journal_write.py 600-616",
      "docs/TESTING.md 213-235; .github/workflows/driver-golden.yml.proposed; scenario-clock.yml 80-104"
    ],
    "reruns": [
      {"command": "pytest test_probe_marker_judgment.py -k publish_failure or stray_flag or refusals_name_the_door (RD1-37 wt)", "result": "3 passed, 47 deselected in 2.28s"},
      {"command": "pytest test_red_sandbox_probe.py --collect-only", "result": "no tests collected"},
      {"command": "python -c test_red_sandbox_probe.no_row_language_reaches_a_counted_receipt()", "result": "rs-probe-one: 12/12 ok"},
      {"command": "scratch main() with --judge --product missing --task, and lone --product", "result": "2 names --product door: False (both)"},
      {"command": "pytest tools/test_wave.py -k restore_oserror (FG7-85 wt)", "result": "3 passed, 124 deselected in 17.00s"},
      {"command": "scratch test_probe_fg785.py (append L3 then OSError) on FG7-85 and on main", "result": "FG7-85: RC 0, L3 lost, copy deleted; main: RC 1, L3 kept, copy kept"},
      {"command": "pytest tools/test_journal_validator.py -k verdict_before_returned (FG7-22 wt)", "result": "9 passed, 319 deselected in 0.58s"},
      {"command": "scratch fg722_probe.py over logs/journal/dev1.jsonl", "result": "warns 104: 99 no returned anywhere, 4 returned after the verdict, 1 resumed ref under another task"},
      {"command": "yaml.safe_load driver-golden.yml.proposed", "result": "defaults {'run': {'shell': 'bash'}}, no step shell override"}
    ]
  }
}
```
