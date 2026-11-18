# t-1464 -- code re-review: FG7-85 fix round (t-1461), RD1-37 S3 fix round 2 (t-1462)

## Verdicts, one per node (inputs to the Lead's acceptance; the decision is the Lead's, rule 6)

- **FG7-85** (cd8d8ea7..a7e6bc04, worktree agent-a45c050000e760235): **ACCEPT** (fit), 0 blocking. P1, P2 and P3 of t-1454 are fixed. I re-ran my P1 scratch scenario on the new tree: rc 1, L3 kept on disk, copy kept. The HEAD-absent case and the failed kept-target write after a merge both refuse safely and lose no byte.
- **RD1-37 S3 fix 2** (1b49cd55 only; the merge be54936b is not judged): **ACCEPT** (fit), 0 blocking. R1, R2 and R3 are fixed, and the R4 report line is corrected. A control run shows that the R2 row now fails when the product door is dropped.

Both nodes are fit, so the JSON block says `fit`. Below: one request about the mechanical layer (M1) and two notes (N1, N2). None of them is a builder finding.

## Findings

No blocking finding, and no fix-before-merge finding, on either node.

**M1 (both nodes, request to the dispatcher; rule 21, mechanical layer).** Neither handoff carries a `red-before:` line, but P1, R1 and R2 are defect items. I did not treat this as a builder finding, because the red is already established from other carriers:
- P1: the t-1454 scratch run of the same input on the old tree gave `RC 0 ... L3 anywhere: False`, and row `appended` asserts `rc == 1` before anything else.
- R2: my control run below. With the door dropped, the row fails at `test_probe_marker_judgment.py:343`.
- R1: the old code printed `JUDGE_DOOR` (t-1454 scratch: `2 names --product door: False`). The new asserts `(JUDGE_PRODUCT_DOOR in error) is bool(args.product)` and `JUDGE_PRODUCT_DOOR in out["error"]` could not pass against that text.

Whether a missing line is waived for a fix round is the Lead's call.

**N1 (FG7-85, note for the Lead, not a builder finding).** After the new refusal "the journal changed inside the window", the E6 hint still says "stage <rel> and fast-forward the root by hand". Two cases:
- P1 case: the journal on disk is `L1+L3` and differs from the copy. If a person follows the hint, git refuses the ff because the index differs from both HEAD and the target. That is a refusal, not a loss.
- Case after a merge (KM below): the root is already fast-forwarded and the disk already holds the right target `L1+L2+L3`. Staging it is harmless but not needed.

t-1454's fix text prescribed "the copy and the hint stay", so the builder did what it was told. Whether the hint should drop in this branch is a separate question for the Lead (FG7-82 E6 text).

**N2 (FG7-85, note).** On the `ff_refused` and `git add failed` roads, the copy has already been written back and staged. The root is left with the journal staged, so the next `wave` refresh refuses with "the journal has staged changes" until a person fast-forwards. No byte is lost, and this is what the hint asks for. This behaviour comes from round 1 (t-1454 Q2 accepted it), and the docstring's "otherwise the copy stays" stays true.

## Standing questions -- FG7-85 fix

- **Q1 (fit to t-1454 P1-P3):**
  - P1: `wave.py:556-563`. `_auto_refresh` now reads the current bytes and handles three cases:
    - equal to the copy: no write;
    - equal to `HEAD:<rel>`, or absent when HEAD lacks it: write the copy;
    - anything else: return "the journal changed inside the window" (copy and hint kept, exit 1).
  - My scratch reruns on a7e6bc04 (the fixtures of `tools/test_wave.py` imported as they are), one world per scenario:
    - **P1** (L3 appended in the window, then OSError): `RC 1` / `REASON [' the journal changed inside the window']` / `ROOT-JOURNAL b'{"n":1}\n{"n":3}\n'` / `COPIES [b'{"n":1}\n{"n":2}\n']`. As expected: rc 1, L3 on disk, copy kept.
    - **HEAD-absent, plain** (journal `dev2.jsonl`, untracked in HEAD; in the window `HEAD has rel2: False disk exists: False`): `RC 0` / `ROOT-JOURNAL b'{"n":1}\n{"n":2}\n'` / `COPIES []` / `STATUS ''`. Nothing is lost: the copy is written and committed by the ff.
    - **HEAD-absent, appended** (an unlocked writer creates the file with L3): `RC 1` / `ROOT-JOURNAL b'{"n":3}\n'` / `COPIES [b'{"n":1}\n{"n":2}\n']` / `STATUS '?? ...dev2.jsonl'`. Both halves survive.
    - **KM** (the swap's ff merge returns 0, an unlocked writer appends L3 right after it, and the kept-target `_atomic_write` raises OSError): `RC 1` / `REASON [' the journal changed inside the window']` / `ROOT-JOURNAL ...{"n":3}\n` / `COPIES [L1+L2]` / `HEAD-JOURNAL L1+L2`. The tail `swap` computed is on disk, not dropped.
    - **First KM attempt** (my hook was not scoped to the swap's merge, so the append landed before step 8 committed it): `RC 0`, with L3 committed. That is a correct outcome for a different input, and I re-scoped the hook.
  - P2: rows `staged` and `ff_refused` (`test_wave.py:444-448`), each asserting its reason, rc 1 and the copy kept. `ff_refused` also asserts that git's text names `f.txt`.
  - P3: `wave.py:37-39` names the FG7-85 branch, its trigger (OSError on write-back, copy equals origin's journal) and its three preconditions.
- **Q2 (builder's choices):**
  - "now == want -> no write" is safe.
  - A failing `git show HEAD:<rel>` is compared as "absent". With a file on disk that differs from the copy, this refuses. With no file, there is nothing to lose. Both directions are safe.
  - A read OSError is caught and becomes a refusal.
  - The check-then-write gap is the same TOCTOU class as `swap`'s own `left` read. After the write, an append that lands before `git add` makes the ff-only merge refuse (the index differs from H and M). One that lands after `git add` stays unstaged on disk. In both cases nothing is lost.
- **Q3 (seams):** additive inside `_auto_refresh`. The swap branches and the hint are untouched.
- **Q4 (class):** sibling `swap()` Q5a carry-over (dispatch `siblings:`). Both writers of the copy over the journal now guard against a changed file. `swap` carries the tail over, and `_auto_refresh` refuses; both are safe. Grep `copy.read_bytes|_atomic_write(` over `wave.py` finds the sites 499, 518, 556/563 and 578. The positive control is the known swap sites 499/518. No third writer. `wave-copy` appears only in `wave.py:491` among non-test tools.
- **Q5:**
  - (a) Row `appended` kills P1: without the guard the copy is written and the ff succeeds, so the run gives rc 0 and `assert rc == 1` fails.
  - (b) The reason texts trace to t-1454 P1 ("the journal changed inside the window") and t-1448's named edge. `endswith(L3)` traces to the P1 fix text "L3 still on disk or in the copy". An exact `== L1 + L3` would be stronger, but this is not a finding.
  - (c) Each refusal reason now has a row.
  - (d) The two old asserts were generalised; `off_main` is still covered.
  - (e) None.
  - (f) VOLUME: the round alone is +17/-3 test against +11/-2 product, but the rule is per node branch (`docs/TESTING.md:215`). `git diff --numstat origin/main...a7e6bc04` gives test +28/-6 against product +42/-2, which is within budget.
  - (g) No new file.
- **Q6:** `git_bytes(root, "show", "HEAD:" + rel)` appears twice (`swap:497`, `_auto_refresh:559`), and each is an inline git call. No helper exists to reuse. Not a finding.
- **Q7:** `_auto_refresh` is about 28 lines with nesting 2. No dead branch.
- **Q8:** a forge tool, not the package.
- **Q9:** no ratchet file in the numstat.
- **Q10:** the forge `wave.py` is outside the package AR map (t-1454 grep, unchanged). VARIETY: n/a.
- **Q11:** none, a byte compare.
- **Q12:** none found (no language, runner or project name in the diff, read in full).

## Standing questions -- RD1-37 S3 fix 2 (1b49cd55)

- **Q1 (fit to R1-R4):**
  - R1:
    - `probe_by_code.py:7978` sets `door = JUDGE_PRODUCT_DOOR if args.product else JUDGE_DOOR` and uses it for `--s6-close` (:7982) and for the missing flags (:7985);
    - `:8410` prints the product door when `--product` is among the stray flags (`stray` holds the flag names, :8406-8407).
    - The live text is byte for byte the same (the same `JUDGE_DOOR` when product is false).
  - R2: the `dispatch` entry builds its world with `open_dispatch=False` and is included in the product-door assert (:343).
  - R3: the test goes through `judge_record(..., product=True)` and asserts `intended_failure` in both the return and the stored record, the receipt file present, and the `manifest_put.py: not run` note carrying the exception name. The note exists only when the `except` fired, so the row also proves the publish road was reached.
  - R4: the report line is corrected.
- **Q2:** a combined stray (`--verdict` plus `--product`) prints the product door, which is the safe direction.
- **Q3:** additive. `_judge_cli` has one caller (`main`, :8405), whose parser always sets `product`. The test namespaces gained `product=False`.
- **Q4 (class, surface "door text of a refusal on the --product road"):**
  - grep `JUDGE_DOOR|JUDGE_PRODUCT_DOOR` over `probe_by_code.py` lists every product-road refusal, and each now prints the product door: 7869 (`_product_judged_record`), 7896/7897, 7905, 7941, 7978-7985, 8410.
  - The remaining `JUDGE_DOOR` sites (3238-3413, 6332, 7760 in the live-only `_judged_record`, and `window_record.py`) are live-road texts.
  - The `story_root` ValueError refusal prints no door.
  - Siblings `_judge_input` and `_demand_critic_dispatch` took the door in t-1445, and both are checked by the D4/D5/dispatch rows.
- **Q5:**
  - (a) Control run: with `_demand_critic_dispatch` wrapped to drop the door, the row fails, `1 failed, 49 deselected` at `:343`. R1 is killed by the `is bool(args.product)` assert and the stray assert.
  - (b) The values are the derived constant `JUDGE_PRODUCT_DOOR` and the D14 outcome.
  - (c) R1, R2 and R3 each have a row.
  - (d) R3's rewrite still checks the same note and also checks the door outcome.
  - (e) None: the `_judge_cli` row and the `judge_record` rows are different doors.
  - (f) VOLUME: the commit is +18/-11 test against +4/-3 product. The node branch (`git diff --numstat origin/main...1b49cd55`, merge base c3f525ed) is test +98 against product +203 plus text lines, which is within budget.
  - (g) No new file.
- **Q6:** the door strings stay derived. No second text.
- **Q7:** none.
- **Q8:** the added lines have 0 non-ASCII characters (positive control: the same grep finds 1 in commit 1d4a3350's subject). The EOL is unchanged: numstat shows 7 changed lines of `probe_by_code.py`, not a whole-file flip.
- **Q9:** no ratchet file in the commit.
- **Q10:** the commit names AR-14. The door constant stays the one `JUDGE_DOOR` plus its derived suffix (AR-13). VARIETY: printed text only; no block or default on an unknown value.
- **Q11:** none. The commit says `judgment: none`, and the diff only changes printed text and tests.
- **Q12:** none found (no language or runner names in the 32-line diff, read in full).

## Spot-checks

- The FG7-85 witness `9 passed, 121 deselected` (-k restore) matches my `-k restore_oserror` run: 6 passed, 124 deselected, 130 in total both ways.
- The RD1-37 witness `50 passed` matches my narrow run: 4 passed, 46 deselected, 50 in total.
- The FG7-85 handoff says "Staged, not committed", but commit a7e6bc04 holds exactly those two files plus the handoff (diff --stat). The Lead's commit; no content gap.

## Trail

- Read:
  - t-1454 review (full); handoffs t-1461 and t-1462;
  - `git diff cd8d8ea7..a7e6bc04 -- tools/` and `git show 1b49cd55 -- ai-packages/` (full);
  - `wave.py:26-40`, `90-130`, `440-595`; `test_wave.py:1-95`, `400-470`;
  - `probe_by_code.py:7735-7766`, `7836-8012`, `8392-8412`; `test_probe_marker_judgment.py:1-40`, `95-125`;
  - `docs/TESTING.md:213-235`; `tools/critic_verdict.schema.json`.
- Commands (verbatim tails):
  - scratch python stdin run on the FG7-85 tree (P1, HA-plain, HA-append), then a re-scoped one (KM, P1): the lines quoted in Q1;
  - `python -m pytest <wt>/tools/test_wave.py -q -k restore_oserror` gives `6 passed, 124 deselected in 66.79s`;
  - `python -m pytest <wt>/.../test_probe_marker_judgment.py -q -k "refusals_name_the_door or publish_failure or stray_flag or s6_close_and_missing"` gives `4 passed, 46 deselected in 3.92s`;
  - R2 control (pytest.main with `_demand_critic_dispatch` dropping its door) gives `1 failed, 49 deselected in 3.60s`, assert at :343;
  - numstat lines as quoted in Q5(f).

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "FG7-85: both writers of the wave copy over the root journal (swap 499/518 and _auto_refresh 556-563, grep with the swap sites as positive control) now guard a journal changed inside the window: swap carries the tail, _auto_refresh refuses; no third writer (wave-copy only at wave.py:491). RD1-37: surface 'door text of a --product refusal' walked by grep JUDGE_DOOR|JUDGE_PRODUCT_DOOR: every product-road refusal (7869, 7896-7897, 7905, 7941, 7978-7985, 8410) prints the product door; the remaining JUDGE_DOOR sites are live-road only.",
  "fixes": [],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1454-rd1-37fix-b3fix-fg7-85-fg7-22-code.md",
      "handoffs t-1461-fg7-85-fix.md, t-1462-rd1-37-s3-fix2.md",
      "FG7-85 diff cd8d8ea7..a7e6bc04; tools/wave.py 26-40, 90-130, 440-595; tools/test_wave.py 1-95, 400-470",
      "RD1-37 commit 1b49cd55; probe_by_code.py 7735-7766, 7836-8012, 8392-8412; test_probe_marker_judgment.py 1-40, 95-125",
      "docs/TESTING.md 213-235; tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "scratch python stdin, FG7-85 tree: P1 (append L3 then OSError)", "result": "RC 1, reason the journal changed inside the window, disk L1+L3, copy L1+L2"},
      {"command": "scratch python stdin, FG7-85 tree: HEAD-absent plain / appended", "result": "plain RC 0 disk L1+L2 status clean; appended RC 1 disk L3 copy L1+L2"},
      {"command": "scratch python stdin, FG7-85 tree: KM (ff ok, L3 appended, kept-target write OSError)", "result": "RC 1, reason the journal changed inside the window, disk L1+L2+L3, copy L1+L2, HEAD L1+L2"},
      {"command": "python -m pytest tools/test_wave.py -q -k restore_oserror (FG7-85 wt)", "result": "6 passed, 124 deselected in 66.79s"},
      {"command": "python -m pytest test_probe_marker_judgment.py -q -k refusals_name_the_door or publish_failure or stray_flag or s6_close_and_missing (RD1-37 wt)", "result": "4 passed, 46 deselected in 3.92s"},
      {"command": "pytest.main with _demand_critic_dispatch dropping the product door, -k refusals_name_the_door", "result": "1 failed, 49 deselected in 3.60s (assert at :343)"},
      {"command": "git diff --numstat origin/main...a7e6bc04 and origin/main...1b49cd55", "result": "FG7-85 test +28/-6 vs product +42/-2; RD1-37 test +98 vs product +203 plus text"}
    ]
  }
}
```
