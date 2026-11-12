# t-041 / PC2-4 — critic on the plan

Spec under review: `docs/tasks/specs/t-041-pc2-4-probe-receipt-and-repeat.md` (with the Lead's «Answers to the forks», 12.11.2026).
Reviewer: critic (Opus), 12.11.2026. Paths below are under `ai-packages/qa-factory/` unless absolute; PBC = `scripts/probe_by_code.py`, PL = `scripts/proof_level.py`, T = `scripts/tests/test_probe_by_code.py`.

## Verdict

**ACCEPT WITH FIXES** (NEEDS WORK for the spec, before dispatch). One blocking finding (B1: F2 as written makes every repeat of a plan holding a `product` row walk forever — B3 lost for that class, silently, no pin turns red). Three non-blocking fixes (N1-N4). The premise of §1/§2 is confirmed by the control run: all six FAIL lines carry exactly the values the designer predicted, including `('no_failure', 1)` for the «incomplete» group. Acceptance of the spec stays with the Lead (rule 6).

## Control run (the premise of §1/§2)

`python -B C:\QAFactory\forge-repo\ai-packages\qa-factory\scripts\tests\test_probe_by_code.py` — run ONCE, background, output in `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\a3462969-9db0-4fa2-b7e5-85b7f9fbbd73\scratchpad\probe_run.txt`. Total line: `=== test_probe_by_code: 756/762 ok ===` (exit 1), 6 FAIL lines. Verbatim (the two long key-set lists are cut where marked; the `got` tail of the first is quoted separately):

```
FAIL pinned invert: the written record's key set — expected ['actual_location', ... 'verdict', 'window_probe', 'words'], got ['actual_location', ... 'instance_identity', 'judgment_owed', 'manifest_fields_missing', ... 'verdict', 'walk_ended', 'window_probe', 'words']
FAIL pinned invert: its notes — expected ["command, fingerprint file list and runtime probe are those of this story's last typed run on profile unit"], got ["command, fingerprint file list and runtime probe are those of this story's last typed run on profile unit", 'work/sensitivity-receipts/test_add-live-e401bc033bfb2f16.json already holds this proof']
FAIL pinned answer: exit 0, the walk answers with the aggregate again — expected (0, 'intended_failure'), got (0, 'already_probed')
FAIL pinned answer: the key set is the aggregate's — expected ['actual_location', ... 'words'], got ['block', 'by', 'holds', 'instance_id', 'level', 'notes', 'prior_verdict', 'receipt_ref', 'record', 'recorded_at', 'verdict', 'words']
FAIL a corrupt record: the check is not proved, so the probe runs again — expected ('intended_failure', 2), got ('already_probed', 1)
FAIL an incomplete record does not answer a repeat: the probe runs — expected ('no_failure', 2), got ('no_failure', 1)
```

The full `got` of the first line differs from `INVERT_RECORD_KEYS` by exactly `judgment_owed` (between `instance_identity` and `manifest_fields_missing`) and `walk_ended` (between `verdict` and `window_probe`) — the §4 positions. The `got` of the fourth equals `sorted(ANSWER_KEYS + ["notes"])` — the F1 (a) repin is the real answer shape.

## Blocking findings

### B1 — F2 (a) never answers a repeat of a plan with a `product` row (surface: the repeat answer, `_repeat_same_entries`)

What. F2 (a) (§6 «F2 in code», E5) requires, for every receipt row with `verdict == "intended_failure"`, a readable per-check record with `verdict: intended_failure` and the same `entry_sha`. A row proved by a `product` entry (EP-W) is `intended_failure` in the aggregate (PBC :6652-6659, `proved_by: critic`, "no run of this call") and so in the receipt's `checks[]` (`_receipt_core` copies every row, PBC :6017-6023), but it NEVER has a per-check record: the walk drops `not_here`/`product` keys before `live` (PBC :6380-6381), `write()` writes only keys in `outcomes` (PBC :6486-6494), and the only other `_check_record` writer is `judge_record` (PBC :7837), for judged rows. Search: Grep `_check_record\(` over PBC → only :5985 (def), :6492, :7837 (positive control: the def line itself is found by the same pattern).

Failure scenario (traced). Plan with one `invert` row + one `product` row whose receipt holds. Call 1: walk proves the invert row, product row `intended_failure` → complete → receipt (PBC :6910-6913). Call 2: `_repeat_look` hits by receipt (PL :1448-1478), `_repeat_is_new` True (PBC :7278), `_repeat_same_entries` today → True → `already_probed`. Under F2 (a): the product row's `_read_check_record` → None → False → walk: product dropped, invert row proved by standing → no group → publish at :6457 → `attach_receipt` → note «already holds this proof». Call 3, 4, ...: identical. The repeat is never answered, every call takes the lock and rewrites the aggregate, and the "already holds" note — the very symptom PC2-4 removes — returns on every repeat. A product-only plan is the pure case (the no-live-key path, PBC :7453, writes the aggregate + receipt each time). This breaks B3 (spec t-2064 :541 "all proved and the aggregate standing: `already_probed` as today") and the stated requirement in `references/field-producers.json:73` ("a probe of unchanged bytes and the same entries is answered `already_probed`"). No existing pin catches it: Grep `kind.{0,4}product` over `scripts/tests/test_probe_*.py` → only `test_probe_product_publish.py`, `test_probe_readers.py`, `test_probe_by_code_alternative.py`; the product-publish repeats are the red_sandbox road (`kind="product"`, lines 145-176), not a walk repeat through `_probe_plan`. So K2 would stay green over a real regression.

E5 names `not_owed` rows as exempt ("they never run") but is silent on `product` rows that are `intended_failure` without a run — an edge the spec's own condition creates (CLAUDE.md rule 11 DoD: an edge its own requirements create).

Fix required (in the spec, before dispatch): the F2 condition applies only to rows the WALK proves, i.e. rows whose entry kind is one the walk runs (`actual` / `find` / `invert`); a row whose entry is `product` stands on its product receipt and is not read here. The spec must say WHERE the kind comes from, since the receipt row carries no kind (PBC :6021-6022): the picked entry of the window's models file (`picked`, already built in `_repeat_same_entries` :7298), and for a check with no entry in the file (the function's docstring: "stands on the one the receipt holds") the stored aggregate's `checks[].entry.kind` / `checks[].product` (the aggregate path is `answer["record"]`) — or, simpler and on the safe side, "no picked entry → read the per-check record as for a walked row" only if the Lead accepts that a product row with its entry removed from the file walks. Add the case to E5 as a row (expected: answered, `already_probed`), and add a variant to an existing parameterised check or name it a live-proof line if no existing check can carry it (K3 forbids a new function — the Lead decides which).

## Non-blocking findings (fixes of this round, not deferred lines)

- **N1 — AR-13 spelling of the read (§6 «F2 in code», K4).** The spec hand-builds `_read_check_record(ctx.task_root, _records_id(ctx), check["line"], _ordinal_of(check), check.get("file"))`. That is byte for byte `_per_check_read(ctx, check)` (PBC :6614-6617), the wrapper `_aggregate_rows` (:6674, :6684) and the judge (:7623, :7656) already use. Require `_per_check_read(ctx, check)`: one spelling of "this check's record", not a second hand-built one (AR-13 / P31). K4's "goes through `_read_check_record`" stays true.
- **N2 — §6 handoff contradicts the Lead's answer.** The node block still says "the commit hash on `pile/package-ci/batch-2`", and K5 asks for a commit message; the answer says the builder does not commit, the Lead commits. Edit the node so the Sonnet builder reads one instruction: no commit; K5 moves to the Lead's acceptance step (or is phrased as "the builder proposes the `architecture:`/`judgment:` lines in the report").
- **N3 — DoD witness scope.** `scenario_walk.py --witness-for` on the owns prints 37 files for PBC, including three scenario tests and `test_story_run_s6.py` (a `test_story_run_*` slow file that PROJECT.md «Как принимается изменение пакета» p. 2 says is not run locally). State which printed files the builder runs locally and which are left to the batch canon, so the builder does not choose. `test_probe_word_repeat.py` and `test_probe_by_code_languages.py` (:1079-1084) exercise the repeat through `_repeat_same_entries` end to end — they ARE in the printed list; name them in K2 next to `test_probe_fix_round.py` so the before/after FAIL comparison covers them.
- **N4 — F1 repin duplicates two existing pins.** After F1 (a) the «pinned answer» checks pin the B3 answer a third time (T :2384-2386 «twice», `test_probe_fix_round.py:188`). The exact key-set equality is the one new fact they add (the «twice» check is a subset test, T :2385-2386), so keeping them is defensible as the B-426 D1 characterisation; say so in the rewritten comment, or drop the verdict line and keep only the key set (Lead's call; no new function either way).

## Answers to the six questions

### Q1 — Facts. Verdict: TRUE (all load-bearing claims hold).
- B3: PBC :7416 comment "fix round A, B3: the old road's one question, before `_entries_for`"; :7417-7421 answer via `_repeat_is_new` / `_repeat_same_entries` / `_repeat_answer`. Green pins read: `test_probe_fix_round.py:172-193`, T :1359-1365. Spec t-2064 :541 item 4 read.
- F3: PBC :6030 `_CARRIED_VERDICTS = ("no_failure", "wrong_location")`, :6450-6452 carry; spec t-2064 :824 read ("Any other stored verdict (`incomplete`, ...) reruns"). Pin `test_probe_fix_round.py:196-208`, T :2454-2459.
- In-loop publish: PBC :6529-6532 `write(...)`, `publish()`, `if result["ended"]: break`; end publish :6549; no-group publish :6457. The intermediate publish cannot attach a receipt: unrun live keys are neither in `outcomes` nor `proved`/`carried` → `not_reached` (PBC :6699-6700) → `_aggregate_verdict` returns `incomplete` (:6722-6728) → :6910 not reached. A rerun-word key stays live (:6448-6449) and also reads `not_reached` until run — confirmed no early receipt. Double write mechanism: `write_receipt` :4067-4076 returns «already holds this proof» when the file exists; `attach_receipt` :4140-4141 appends it to the record's notes. Confirmed by the control run's notes FAIL line.
- Readers: Grep `judgment_owed|walk_ended` (case-insensitive) over `ai-packages/qa-factory` → PL :1123-1126 (`probe_record_state`), PL :1170-1174 (`probe_plain_call_owed`), PBC :7795 (`_refold`); producers PBC :6752, :6890 found by the same search (positive control). Plus test pins in `test_probe_every_check.py`, `test_probe_judge_languages.py:49`, `test_probe_product_publish.py:211-235`.
- §2 trace of the «corrupt» and «incomplete» groups: confirmed by reading PL :1448-1532 (item 1 does not need the aggregate when the receipt carries `mutated_file`, :1468-1470; item 2 sees the stamped `incomplete` and does not hit, :1491) and by the control run values.

### Q2 — §3 one write per walk, "a killed walk keeps both". Verdict: KEPT, with one narrow, self-healing loss (already stated in E3).
- Intermediate groups: unchanged (publish after the per-check records of every group but the last).
- Last group of a complete walk: the in-loop publish is removed; between `write(group, ...)` and the :6549 publish there is only in-memory work and `write(remaining)` (empty for a complete walk). A kill in that window leaves the per-check records of the last group and the previous group's aggregate (none for a one-group walk), no receipt. Next call: every check proved by standing → no group → :6457 publish writes the receipt. Self-heals; before the change the same window existed between `write` and the in-loop publish.
- Ended walk (time / stop / restore_failed): the in-loop publish before `break` is gone, so a kill between `break` and :6549 loses the on-disk aggregate that would have recorded `walk_ended` and `restore.error` + `copy`/`file`/`author_sha256` (PBC :6840-6843). The dead copy is still settled by `_settle_dead_copy` at the next call (PBC :7405), and the per-check records carry the row outcomes. Not blocking (microsecond window, recovery path exists); the spec's E3 says "the aggregate never leads the per-check records", which holds.
- An exception (not a kill) in the tail (:6533-6548, e.g. in `_walk_stamp`) now loses this walk's receipt where the old in-loop publish had written it; same self-heal as above. Acceptable.

### Q3 — F2 (a). Verdict: right error side for walked rows; second reader: no (with N1); loop: YES for `product` rows — B1.
- Error side: every doubt (absent, unreadable, non-object, other verdict, other `entry_sha`) → False → walk (FR-59, AR-28). Correct direction. Convergence for walked rows: the walk rewrites the per-check records it runs, and a carried/proved one already agrees, so the next repeat is answered (traced via :6443-6452, :6486-6494).
- Second reader: it reads through `_read_check_record`, the declared one reader (PBC :6033-6036); use the existing wrapper `_per_check_read` (N1). Its condition (verdict + `entry_sha`) is a strict weakening of `_check_standing` (no bytes key, no flags) — legitimate because item 1 of `already_probed` already binds the receipt to these bytes; worth one sentence in the docstring so a later reader does not "unify" it into `_check_standing` and drop the receipt's byte role.
- Loop: B1. Rows with entry kind `product` are `intended_failure` with no per-check record by construction → the repeat is never answered.

### Q4 — FR-58 for F1 (a) and F3 (a). Verdict: both test a named requirement, not the code.
- F1 (a): the expected `already_probed` comes from B3 (spec t-2064 :541; the fix-round decision at PBC :7416) and `field-producers.json:73`; the key set is `_repeat_answer`'s shape, which is the old road's answer shape the spec names (`_repeat_check`, PBC :7309). The pins at T :2332-2337 carried an open "question for the coordinator" that B3 answered. See N4 on duplication.
- F3 (a): the expectation `('no_failure', 2)` stays and the fixture moves to the record the walk reads; the requirement is spec t-2064 :824 ("Any other stored verdict (`incomplete`, ...) reruns") and B-373 R10 (T :2514-2516: a stored `incomplete` is never a standing verdict). After the edit the check would go red if `incomplete` were added to `_CARRIED_VERDICTS` — it tests the requirement. Note: the aggregate stamp in that group becomes decorative (item 2 never hits either way); the rewritten comment should say the per-check record is the subject.

### Q5 — AR-n / FR-n / P31. Verdict: AR-13, 14, 22, 29 kept; AR-28 kept in direction but B1 breaks the requirement B3 rests on; nothing material unnamed.
- AR-14: `_aggregate_record` and `write_receipt` stay single writers (Grep `attach_receipt\(|_aggregate_record\(` → callers PBC :4709, :6409, :6913, :7453, :7799, :7849; no new writer).
- AR-22: both keys have readers (Q1); none removed.
- AR-13: kept with N1.
- AR-28: F2 errs only toward walking.
- AR-29: F2 is a data check (presence/equality), no judgment.
- Unnamed: FR-59 is named in F2; AR-25 (every returned state a move) — the walk answer remains a move; not touched. The judgment census row: `_repeat_same_entries` has none (Grep in `judgment-census.json` → only `_repeat_check` :614) and gate-registry names `already_probed` only (:129); K4's STOP rules cover a surprise.
- P31 (critic-diff-brief item 12): one road for "is this check proved" stays `_check_standing` on the walk; F2 asks a different question (does the stored record agree with the receipt) through the same reader. No exclusion of a language/project/case is introduced — EXCEPT the implicit one B1 creates (plans with a `product` row lose the repeat answer); fixing B1 removes it.

### Q6 — Builder node executability. Verdict: executable after B1 and N2; otherwise complete.
- Owns by function: yes (`_walk_plan`, `_repeat_same_entries`; two test functions + `INVERT_RECORD_KEYS`; changelog fragment).
- Edges E1-E7 each have an expected behaviour and invariant; E5 is missing the `product` row (B1).
- Step 0 has a precise STOP condition; my control run already shows its expected values (the builder still records its own, as written).
- DoD run named; scope needs N3. Handoff/commit contradiction: N2.

## Standing questions

- DUPLICATION AND CONSISTENCY: N1 (hand-built read beside the existing `_per_check_read`), N4 (third pin of B3). Grepped: `_per_check_read\(|_read_check_record\(` over `scripts/`; `already_probed` over the probe test files.
- CODE QUALITY: none found in the plan beyond N1/N2 (a plan gate; existing code not reviewed by instruction).
- ONE ACTION, ONE ROAD (P31): see Q5 — the only exclusion is the one B1 introduces; fix of this round.

## Class completeness

Rule 5 / map: `docs/SIBLING_MAP.md` has no axis for the repeat answer or the receipt writers (Grep `already_probed|sensitivity-receipt|repeat question|red_sandbox`, case-insensitive → only lines 142/148/154/190, report-row readers, assertion-probe table and other axes, none about the repeat). Artifact sweep instead: (a) the repeated-receipt class — every `_aggregate_record` caller in one call: walk (:6409, now one receipt-capable call per walk), no-live-key path (:7453, once), `_refold` (:7799, once per judge) — no other double call; (b) the "repeat answered over a damaged/absent record" class — the EP-I branch (:7417-7419) answers old single records that have no per-check records by design (n/a), `_repeat_check` (:4474) is called only by `test_probe_one_road.py` (Grep `_repeat_check\(`), not by the road; `_repeat_same_entries` is the only walk-record answerer — covered by F2, with B1.

## Trail

Read: the spec (whole); finding path from the dispatch (not opened: the spec quotes it and the Lead's brief is in the dispatch); PBC :3995-4144, :4690-4712, :6026-6090, :6380-6569, :6620-6739, :6735-6918, :7236-7435, :7780-7852, :8290-8330; PL :1404-1533; T :2280-2539, :1355-1384; `test_probe_fix_round.py:172-209`; `test_probe_product_publish.py:100-199`; `test_red_sandbox_probe.py:420-454`; spec t-2064 :541, :824 (and line 20 — note: its table row "B3" is the `--at` road, a different B3 from the fix-round B3 the code comment names; harmless, the spec cites the right one by line); `tools/critic_verdict.schema.json`.
Greps (all with positive controls named above): `judgment_owed|walk_ended` (-i); `_check_record\(`; `_per_check_read\(|_read_check_record\(`; `attach_receipt\(|_aggregate_record\(`; `_repeat_check\(`; `kind.{0,4}product` in `test_probe_*.py`; `already_probed|_repeat_same_entries` in eight probe test files; `_repeat_same_entries|_repeat_check|already_probed` in package `*.json`; SIBLING_MAP for the repeat axis.
Runs: the control run above (once); `python -B ...\scenario_walk.py --witness-for ai-packages/qa-factory/scripts/probe_by_code.py ai-packages/qa-factory/scripts/tests/test_probe_by_code.py` → 37 rows for PBC (3 scenario, 34 keep incl. `test_story_run_s6.py`, `test_probe_word_repeat.py`, `test_probe_by_code_languages.py`), 3 for T.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: F2 (a) requires a readable per-check record for every intended_failure receipt row, but a row proved by a product entry (PBC :6652-6659) never has one (dropped before live :6380-6381; per-check writers only :6492, :7837). Every repeat of a plan with a product row then walks forever, re-attaching the receipt with the 'already holds this proof' note; B3 (t-2064 :541) and field-producers.json:73 broken, no pin turns red. Fix: apply the F2 condition only to rows whose entry kind the walk runs (actual/find/invert); name the source of the kind (picked entry, else the stored aggregate's checks[].entry); add the case to E5."
  ],
  "fixes": [
    "B1 as above (spec edit before dispatch).",
    "N1: the new read uses _per_check_read(ctx, check) (PBC :6614-6617), not a hand-built _read_check_record call.",
    "N2: the node's handoff and K5 match the Lead's answer: the builder does not commit; the architecture/judgment lines go to the Lead.",
    "N3: state which scenario_walk --witness-for files run locally and which go to the batch canon (test_story_run_s6.py is a slow file); name test_probe_word_repeat.py and test_probe_by_code_languages.py in K2.",
    "N4: the F1 repin comment says the exact key set is the value these checks add over T :2384-2386 and test_probe_fix_round.py:188 (or the Lead drops the verdict line)."
  ],
  "class_completeness": "SIBLING_MAP has no repeat/receipt axis (grep -i already_probed|sensitivity-receipt|repeat question|red_sandbox: only unrelated rows). Artifact sweep: all _aggregate_record callers (:6409, :7453, :7799) make one receipt-capable call per call after the fix; repeat answerers: EP-I branch n/a (old records have no per-check records), _repeat_check off the road (only test_probe_one_road.py), _repeat_same_entries covered by F2 with B1.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-041-pc2-4-probe-receipt-and-repeat.md (whole)",
      "ai-packages/qa-factory/scripts/probe_by_code.py :3995-4144, :4690-4712, :6026-6090, :6380-6569, :6620-6918, :7236-7435, :7780-7852, :8290-8330",
      "ai-packages/qa-factory/scripts/proof_level.py :1404-1533",
      "ai-packages/qa-factory/scripts/tests/test_probe_by_code.py :1355-1384, :2280-2539",
      "ai-packages/qa-factory/scripts/tests/test_probe_fix_round.py :172-209",
      "ai-packages/qa-factory/scripts/tests/test_probe_product_publish.py :100-199",
      "ai-packages/qa-factory/scripts/tests/test_red_sandbox_probe.py :420-454",
      "docs/tasks/specs/t-2064-probe-every-check.md :20, :541, :824",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {
        "command": "python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_probe_by_code.py",
        "result": "=== test_probe_by_code: 756/762 ok === ; 6 FAIL lines, values exactly as spec section 1/2 predict (incomplete group: got ('no_failure', 1); key set: extra judgment_owed and walk_ended; answer keys = ANSWER_KEYS + notes)"
      },
      {
        "command": "python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/probe_by_code.py ai-packages/qa-factory/scripts/tests/test_probe_by_code.py",
        "result": "37 rows for probe_by_code.py (3 scenario + 34 keep, incl. test_story_run_s6.py, test_probe_word_repeat.py, test_probe_by_code_languages.py); 3 rows for test_probe_by_code.py"
      }
    ]
  }
}
```
