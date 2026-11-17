# t-1070: why the dry main pass still stops at S5 after N2h-v (diagnosis)

Tree: root checkout `C:/QAFactory/forge-repo`, `main` at 2e9cb3a9 (it contains the N2h-v merge 5408a22f). This is a diagnosis, not a diff review. Nothing in the repo was edited except this file.

## Summary

- **`review.receipt_ref` (K1, K2): PRODUCT GAP.** It does not come from the stub, and it is not a consequence of `runtime_provenance`. In the main pass, `window_record.py` **exits 0** and writes `work/windows/S5-qa-code-critic-1.json` and the review receipt. `handoff_check --fix` still leaves the field blank. The reason: its deriver `_review_receipt` looks for the dispatch id in `doc["header.dispatch"]`, then `doc["dispatch"]`, then `art.dispatch`. The `s5-critic-to-automator` form has no such field. And `Artifacts` never sets `dispatch`: it sets `form_dispatch`, and its own comment says so. So this deriver cannot fill the field on any real critic form. It is a dead deriver.
- **`probes.runtime_provenance` (K3): PRODUCT GAP**, now measured, as the card's A11 predicted. The critic's own probe run carries the record. Its `red_probe` request under `work/probe-requests/` has `dispatch_id: S5-qa-code-critic-1` and `runtime_provenance.evidence_refs` pointing to an existing evidence file. But a `red_probe` writes no run block, and `window_runtime_record` reads run blocks only.
- The two causes are independent. Fixing either one alone leaves the other line, so the pass needs both product fixes to get past S5.

## What I ran (one main pass, the world kept)

I wrote a scratch runner, `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\keep_main.py`. It is `dry_world.main_pass()` with `World.close` patched so that it does not delete the world. Command: `( cd C:/QAFactory/forge-repo/ai-packages/qa-factory && python -B <scratch>/keep_main.py )`, exit 0. Output: `...\scratchpad\keep_main.out`. Verbatim lines:

```
KEPT WORLD ROOT: C:\Users\i_mas\AppData\Local\Temp\qa-story-run-s0-tqwkmqn_
NOTE dry-1/main/known_red known red: main/S5 -> FV3-20
NOTE dry-1/main/stop stopped at S5: the road met the conductor: ... exit gate for S5-qa-code-critic-1 (qa-code-critic, S5): 2 finding(s): - handover form S5-qa-code-critic-1.yaml - review.receipt_ref: not filled. work/windows/<this dispatch>.json, written by window_record.py - handover form S5-qa-code-critic-1.yaml - probes.runtime_provenance: not filled. path of the runtime_provenance record this review probed against Code could not fill it: no run block of dispatch S5-qa-code-critic-1 under work/run-blocks/ carries a runtime_provenance record: ...
NOTE dry-1/main/stub-wrote S5 qa-code-critic (window -): work/probe-models/S5-qa-code-critic-1.json, work/probes/test_the_case.json, work/automation-manifest.json, work/windows/S5-qa-code-critic-1.json, work/handoffs/S5-qa-code-critic-1.yaml
NOTE dry-1/main/time 393.5 s in 4 driver process(es); seconds per stage {'start': 88.4, 'S1': 12.9, 'S2': 26.5, 'S3': 86.4, 'S4': 69.2, 'S5': 103.8}; stages done S0, S1, S2, S3, S4
```

This reproduces the coordinator's symptom: the same 2 findings. Time: 393.5 s. That is under the 800 s stop, so E12 holds.

The kept world is `C:\Users\i_mas\AppData\Local\Temp\qa-story-run-s0-tqwkmqn_` (a temp folder, left for re-reading). In it, `qa-factory/artifacts/DRY-1/state/dry-stub.jsonl` holds the stub's S5 critic row:

```
"window_record": {"exit": 0, "text": "window record: work/windows/S5-qa-code-critic-1.json — 1 instance(s), scope TC-1 note: the probe's target could not be compared with the obligation's assertion (no `assertion_id` of the form `<file>:<line>`) (test_the_case) review receipt: work/review-receipts/S5-qa-code-critic-1.json manifest_put.py: automation-manifest.json: revision 6, receipt 17250b4432ab4c0b80f81050be2a689b the window is acce"}
"probes": [{"instance": "test_the_case", ..., "exit": 0, "text": "probe test_the_case: intended_failure — ... record work/probes/test_the_case.json; evidence evidence/runs/44bcd10c384267c69a56/red_probe-...json; restore verified ..."}]
"fixed": {"exit": 1, "text": "handoff_check: s5-critic-to-automator is not ready - 2 field(s) below. ... review.receipt_ref: not filled. work/windows/<this dispatch>.json, written by window_record.py probes.runtime_provenance: not filled. ..."}
```

Next, I called the derivers directly against the kept world. Script: `...\scratchpad\probe_deriver.py`. It runs in-process, reads only, and writes nothing to the world or to the repo.

```
window file exists: True
doc header.dispatch: None doc dispatch: None
art.form_dispatch: 'S5-qa-code-critic-1' hasattr(art,'dispatch'): False
_review_receipt(art, doc) -> None
_form_dispatch(art, doc) -> 'S5-qa-code-critic-1'
CONTROL with art.dispatch set -> ('work/windows/S5-qa-code-critic-1.json', 'window_record.py wrote it for this dispatch')
window_runtime_record -> (None, "no run block of dispatch S5-qa-code-critic-1 under work/run-blocks/ carries a runtime_provenance record: this dispatch ran no test through run_suite, or its run was refused before it started; the record is written by runtime_probe.py when run_suite runs this dispatch's tests")
```

The CONTROL line is the positive control. With the dispatch id reaching the deriver, the same deriver on the same world returns the window path. So the deriver works, and the input it reads (`art.dispatch`) is the defect.

The world's run blocks: there is exactly **1**, `...66bd1d15b5fe5da442d7.json`, with `dispatch_id: S5-qa-automator-1`, `purpose: initial`, `runtime_provenance.evidence_refs: [.../evidence/runtime-provenance-dry-pytest-20261117T075205Z.json]`. The critic's probe request `work/probe-requests/probe-walk-test_the_case-1.json` has `purpose: red_probe`, `dispatch_id: S5-qa-code-critic-1`, and `runtime_provenance.evidence_refs: [.../evidence/runtime-provenance-dry-pytest-20261117T075205Z.json]`. That evidence file exists.

## K1. Why `review.receipt_ref` is not filled

- `window_record.py` exit code: **0** (window acceptable). It refused nothing: there are **no gaps**. Its output names `review receipt: work/review-receipts/S5-qa-code-critic-1.json` (the receipt file exists), and the manifest was published (revision 6).
- `work/windows/S5-qa-code-critic-1.json` **exists** after the call (`stub-wrote`, and `window file exists: True`).
- The gap is in `handoff_check.py`:
  - `_review_receipt`, `scripts/handoff_check.py:158-170`. Line 164 is `dispatch = str(doc.get("header.dispatch") or doc.get("dispatch") or "").strip()`. Line 166 falls back to `getattr(art, "dispatch", "")`. Line 169 builds `rel = f"work/windows/{dispatch}.json"` only when `dispatch` is non-empty; otherwise line 167 returns `None`.
  - The form carries neither field. The contract `handoffs/s5-critic-to-automator.yaml:32-36` has `header: role, stage, window, verdict` and no `dispatch`. Among all `handoffs/*.yaml`, only `role-to-conductor.yaml:25` has a `dispatch:` field. The grep `^  dispatch:|^dispatch:` over `handoffs/*.yaml` found only that line, which also serves as the positive control.
  - `Artifacts.__init__`, `scripts/handoff_check.py:79-82`, sets only `self.form_dispatch = dispatch`. Its comment reads: "Not `dispatch`: `_review_receipt` reads that name and nothing has ever set it." The fallback reads an attribute that does not exist.
  - The one reader that already exists, `_form_dispatch` (`:173-177`), returns `'S5-qa-code-critic-1'` on this form.
  - Since the deriver returns `None` (no third element), `--fix` prints the bare `not filled. <hint>` with no "Code could not fill it" suffix (`:1645-1677`). That is exactly the line in the symptom.
- Class search: `art\.dispatch|getattr(art, "dispatch"` over `scripts/*.py`, case-insensitive. Its only hit is `handoff_check.py:166`. Positive control of the same shape: `getattr(art, "form_dispatch"` finds `:176` and `:821`. So no other deriver reads the unset attribute.
- Real recorded runs never exercised this deriver. The critic typed the value: `fixtures/stories/cart-1/work/handoffs/S5-qa-code-critic-3.values.applied.yaml:15` and `S5-qa-code-critic-7.values.applied.yaml:4` (`review.receipt_ref: work/windows/S5-qa-code-critic-7.json`). Neither recorded form carries `header.dispatch`. No test in `scripts/tests/test_handoff*.py` drives `_review_receipt` (grep `_review_receipt|receipt_ref`: only two table rows that already *type* `work/windows/x.json`, `test_handoff.py:1575` and `test_handoff_values_main_block.py:56`).

## K2. Classification of `receipt_ref`: (b) PRODUCT GAP

- It is not (a). The stub does what the critic's charter says: "`manifest_put.py --fragment` for review fields, `window_record.py --task <TICKET> --dispatch <your dispatch id> --review-receipt`" (`agents/qa-code-critic.md:69`). The order is the card's (probes → fragment → window_record → form → `--fix`; `dry_stub.py:535-539`, `:954`, `:977`). The tool exited 0 and its file is on disk. Under AR-13 the stub must not type a field that has a deriver, and the card forbids it.
- It is not (c). `window_record` was not refused at all (exit 0, no gaps), and the deriver never reads run blocks. **Fixing runtime provenance alone would NOT fill `receipt_ref`.** It would stay blank with the same text.
- It is (b). The required field `review.receipt_ref` has a producer (`window_record.py`) and a designated reader (`_review_receipt`), and the wiring between them is broken. On every real `s5-critic-to-automator` form the deriver gets no dispatch id, so `--fix` cannot fill the field from a file that exists. The only roads left are typing (which AR-13 forbids, and which recorded roles did) or a person. Rules touched: FR-17 (a tool for the problem, not wired where the problem occurs), AR-13, AR-22, and FR-5 for a stub or any role that does not type. The docstring at `:160-162` even cites TP1-13797 as the reason this deriver exists.

## K3. `probes.runtime_provenance`: (b) PRODUCT GAP, measured

- **Does the critic's dispatch run a test through `run_suite`?** Only as the probe: `probe_by_code.py` runs `run_suite.py --request` with a `red_probe` request (`probe_by_code.py:13-16`). `build_run_block` returns `None` for `purpose == "red_probe"` (`run_suite.py:470-473`). In the world: one run block, of `S5-qa-automator-1`, and none of the critic.
- **Should it run `--mine`?** No. The critic's card (`brief_pack.py:238-258`) lists `probe_by_code`, `red_sandbox --probe`, `RUN_DETAIL` (`run_suite.py --detail`: "no re-run", `brief_pack.py:168-169`), `MANIFEST_VIEW`, `STAND_PROBE` and `s5_precheck`. There is no `RUN_MINE`. The charter (`agents/qa-code-critic.md:69`) names `run_suite.py --request <the record's request> --detail <test>` only "for a red's cause". The contract describes the field as "The stand the probes ran on: the record of this review's own probe run" (`handoffs/s5-critic-to-automator.yaml:53-55`), so it means the probe run, not a suite run.
- **The record exists, but where the deriver does not look.** The critic's own probe request (`work/probe-requests/probe-walk-test_the_case-1.json`, `dispatch_id: S5-qa-code-critic-1`) carries `runtime_provenance.evidence_refs[0]` = `evidence/runtime-provenance-dry-pytest-20261117T075205Z.json`, which exists. `window_runtime_record` (`handoff_check.py:525-580`) reads only `work/run-blocks/` blocks whose `dispatch_id` is this dispatch (`:546-555`). The refusal text `_RECORD_PRODUCER` (`:522`) names a road ("when run_suite runs this dispatch's tests") that the critic is not handed. That breaks FR-2 (the door named must be usable by the refused party). Critic t-1058 key 7 already noted this.
- **Recorded real runs.** No recorded S5 critic ever met the "own run block" demand. The deriver arrived in `bbb21ff4` (2026-11-14), after both recordings:
  - `cart-1` (2026-10-31): all 8 run blocks belong to `S5-qa-automator-{2,3,4,7}` or `S6-qa-runner-1`, none to a critic. The critic forms carry *typed* values: `S5-qa-code-critic-7.yaml:57` names `qa-factory/artifacts/CART-1/evidence/runs/c9286026d096394cd0e6` (the automator-7 run), and `S5-qa-code-critic-4..6.yaml:57` name the *window file*, which is a wrong value.
  - `local-1-0108`: `S5-qa-code-critic-14.yaml:64` types `evidence/runtime-provenance-web-20261102T043727Z.json`, and there are no run blocks recorded (`find local-1-0108 -iname '*run-block*'` is empty; the same find on cart-1 finds `work/run-blocks`).
  - So a real critic passes this field only by typing (the `--fix` loop checks only "blank" and options, `handoff_check.py:1661-1680`; no other script reads `probes.runtime_provenance`: grep `probes.runtime_provenance|window_runtime_record` over `scripts/*.py` hits only `handoff_check.py`). Typing bypasses the one reader (AR-13) and in recordings produced wrong values.
- Classification: **(b) product gap.** The deriver demands a state (a run block of the critic's dispatch with `runtime_provenance`) that nothing on the critic's road produces. The equivalent fact that is produced (the probe request's `runtime_provenance`) is not read. Rules: FR-5, FR-11, AR-22, FR-2.

## K4. Smallest changes, as proposed nodes (not implemented)

**Node P-a: the receipt deriver reads the form's own dispatch.** Owner: a product finding in pile `live-run-fvf`, id issued by the Lead; executed by a builder (one function).
- File and function: `ai-packages/qa-factory/scripts/handoff_check.py`, `_review_receipt` (`:158-170`). It resolves the dispatch through `_form_dispatch(art, doc)` (`:173-177`, the one reader, AR-13), not through `header.dispatch`, `dispatch` and the unset `art.dispatch`. Then delete the stale comment at `:80-81` and the "keeps its own order" remark at `:174`.
- Witness: a table row in `scripts/tests/test_handoff.py` on a `s5-critic-to-automator` form named `<D>.yaml` with no `header.dispatch`:
  - `work/windows/<D>.json` present → `--fix` fills `review.receipt_ref = work/windows/<D>.json`;
  - absent → blank with today's hint;
  - only `work/windows/<other>.json` present → blank. The deriver must never name another dispatch's window.

  Run it with `python -B ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for ai-packages/qa-factory/scripts/handoff_check.py`. Then the dry main pass (`--part main`) prints 1 finding (`probes.runtime_provenance` only) until P-b lands.
- Edge that must not regress: a form whose file stem is not a dispatch id (a `.values.yaml` or an applied copy). `_form_dispatch` already takes the stem first. The invariant: a receipt path is derived only for the form's own dispatch and only from a file that exists.

**Node P-b: a producer that the critic's road can reach for `probes.runtime_provenance`.** Owner: a product finding in pile `live-run-fvf`, id issued by the Lead. It changes the MEANING of a deriver's source, so it needs the designer and a critic on the plan first (PROJECT.md, package change item 6).
- Recommended direction (a fork for the Lead): in `handoff_check.py`, `window_runtime_record` (`:525-580`), when no run block of the dispatch carries a record, read `runtime_provenance.evidence_refs[0]` of the NEWEST `red_probe` request of THIS dispatch under `work/probe-requests/`. Resolve it with the same in-story rule (`:567-580`). This is "the record of this review's own probe run" that the contract names (`s5-critic-to-automator.yaml:53-55`). In the same move, rewrite `_RECORD_PRODUCER` (`:522`) so it names the probe as a door the critic is handed (FR-2).
- Alternative, not recommended: `run_suite` writes a block for `red_probe`. `run_suite.py:470-473` keeps mutated reds out of the ledger on purpose.
- Witness: `test_handoff.py` rows:
  - a probe request of the dispatch, with an existing evidence file → filled;
  - only another dispatch's request → blank;
  - a request whose `evidence_refs` is empty or names a missing file → blank with a named reason.

  Then the dry main pass goes past S5, or prints its next stop verbatim.
- Edge that must not regress: for dispatches that HAVE a run block (automator, runner: `artifacts.runtime_provenance`, `runtime.provenance`, `handoff_check.py:645-651`), the run block keeps precedence and the result is byte-identical. A probe request must never outrank a dispatch's own run block.

**No stub node.** Neither line is a stub gap. The stub must not type either field (AR-13, AR-29). FV3-20's class "stub gap" no longer describes the stop.

## K5. The `raised_by` text the `main/S5` row should carry now

```
product gap: Lead t-1070, 2026-11-17: stopped at S5: exit gate for S5-qa-code-critic-1 (qa-code-critic, S5): 2 finding(s): review.receipt_ref not filled (window_record.py exit 0 wrote work/windows/S5-qa-code-critic-1.json; handoff_check._review_receipt reads header.dispatch/dispatch/art.dispatch, which the form and Artifacts never carry); probes.runtime_provenance not filled (window_runtime_record reads run blocks only; the critic's red_probe writes none, its probe request carries the record)
```

The row's `node` should move from FV3-20 (stub gap) to the product finding(s) the Lead issues for P-a/P-b. That decision belongs to the Lead; `pins.known_red` stays 1. Do not raise the pin unless a second row is added.

## K6. Facts of the card and of critic t-1058 that did not hold

1. **Card A6**, `docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md:15`: "`handoff_check --fix` derives it as `work/windows/<dispatch>.json` only when that file exists". This does not hold. The derivation also needs a dispatch id from `header.dispatch`/`dispatch`/`art.dispatch`, which the critic form and `Artifacts` never carry (`handoff_check.py:164-167`, `:79-82`; measured: `_review_receipt(art, doc) -> None` with the file present). The card cited `:158-170` but did not trace line 164. The same false premise carries:
   - the finding text at `:53` ("(б) — заглушка");
   - the §2.2 invariant at `:182` ("`--fix` derives `review.receipt_ref` only from a file that exists");
   - E10 at `:197` ("The pass stops at S5 with ONE finding").

   This is the fact that made "one finding" fail.
2. **Card A11 and E10 on `runtime_provenance`** (`:20`, `:197`) **held**. They are now measured.
3. **Critic t-1058**, `docs/tasks/specs/reviews/t-1058-p1b-n2h-v-code.md:34` (key 2: "The stub never writes `receipt_ref`; `--fix` derives it") and `:36` (key 4: AR-13 "filled only by handoff_check's derivers"). The review took A6 on faith, without tracing `_review_receipt`'s source of the dispatch id. The trail at `:45` reads `handoff_check.py:522-550` only, not `:158-177`. Key 7 (`:39`) said "The expectation is sound by code" and covered only `runtime_provenance`. Mitigation: F4 (`:21`) did flag that E10 was unmeasured and blocked the merge on obtaining the main lines. The wave merged with the label left at the old 3-finding text.
4. The N2h-v builder report (`docs/tasks/specs/reports/20261117-p1b-n2h-v-report.md:31`) repeats the card's expectation and labels it "NOT RUN". That is honest, not a defect.

## Standing lines

- **DUPLICATION AND CONSISTENCY:** there are two dispatch readers in `handoff_check.py`: `_review_receipt`'s own lookup (`:164-167`) and `_form_dispatch` (`:173-177`). The first is the defect. P-a removes the duplicate. Grepped: `art\.dispatch|getattr(art, "dispatch"` (1 hit) and `header.dispatch` (`:164`, `:177`).
- **CODE QUALITY:** a dead fallback (`getattr(art, "dispatch")`) and a comment that admits it (`:80-81`).
- **ONE ROAD:** the critic's `runtime_provenance` today has only the typing road; P-b gives it the deriver road. No language or project branch is involved.
- **TESTS:** no test drives `_review_receipt` (grep above). P-a and P-b each owe their `test_handoff.py` rows.
- **Class (SIBLING_MAP, the derivers axis):** of all `DERIVERS`, only `_review_receipt` reads the unset attribute (grep above). `window_runtime_record` serves three paths (`:645-651`); P-b must keep the run-block precedence for the two non-critic paths. Not walked: other contracts' derivers that may require fields their own templates lack. That would need a scout question: "for every DERIVERS/BY_PATH entry, does the deriver's input exist on every contract that lists the field?"

## Trail

Read:
- the N2h-v card (whole);
- the N2h-v report (whole);
- critic t-1058 (whole);
- `dry_stub.py:197-209,440-632,905-982`;
- `dry_world.py:255-335,930-1072`;
- `harness.py:232-240,514-526`;
- `test_scenario_dry_1.py:1-60`;
- `window_record.py:1-57,2150-2290`;
- `handoff_check.py:60-100,150-180,515-600,630-665,1625-1690`;
- `agents/qa-code-critic.md:55-100`;
- `handoffs/s5-critic-to-automator.yaml:1-80`;
- `brief_pack.py:145-173,236-260`;
- `run_suite.py:455-485`, grep runtime;
- `probe_by_code.py:1-40`;
- `story.json` row `qa-code-critic@S5`;
- `known_red.json`;
- cart-1 critic forms and run blocks;
- local-1-0108 critic form;
- `git log -S` for `def window_runtime_record` (bbb21ff4) and for the `nothing has ever set it` comment (9ac00f09, the initial import).

Runs:
- one main pass with the world kept (393.5 s);
- the stub journal row read from the world;
- the in-process deriver probe with a positive control;
- run blocks, the probe request and the probe record read from the world.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "PRODUCT GAP P-a: handoff_check._review_receipt (handoff_check.py:164-167) reads header.dispatch/dispatch/art.dispatch; the s5-critic-to-automator form carries none and Artifacts sets only form_dispatch (:79-82), so review.receipt_ref is never derived although window_record.py exit 0 wrote work/windows/S5-qa-code-critic-1.json",
    "PRODUCT GAP P-b: window_runtime_record (handoff_check.py:525-580) reads run blocks only; the critic's red_probe writes none (run_suite.py:470-473) while its probe request under work/probe-requests carries runtime_provenance.evidence_refs of an existing file"
  ],
  "fixes": [
    "P-a (product finding, Lead issues id): _review_receipt resolves the dispatch through _form_dispatch(art, doc); test_handoff rows present/absent/other-dispatch window",
    "P-b (product finding, designer + critic on plan, meaning change): window_runtime_record falls back to the newest red_probe request of THIS dispatch; run blocks keep precedence; _RECORD_PRODUCER names the probe (FR-2)",
    "Label: known_red.json main/S5 raised_by to the K5 text; node moves from FV3-20 (stub gap) to the product finding id; pin stays 1"
  ],
  "class_completeness": "Unset art.dispatch is read only at handoff_check.py:166 (grep art.dispatch / getattr(art, dispatch), control finds form_dispatch at :176,:821); window_runtime_record serves three paths (:645-651), P-b must keep run-block precedence for the two non-critic ones; a scout question is proposed for derivers whose inputs the listing contracts lack",
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-p1b-n2h-v-critic-stub-window-card.md",
      "docs/tasks/specs/reports/20261117-p1b-n2h-v-report.md",
      "docs/tasks/specs/reviews/t-1058-p1b-n2h-v-code.md",
      "ai-packages/qa-factory/scripts/tests/dry_stub.py:197-209,440-632,905-982",
      "ai-packages/qa-factory/scripts/tests/dry_world.py:255-335,930-1072",
      "ai-packages/qa-factory/scripts/window_record.py:1-57,2150-2290",
      "ai-packages/qa-factory/scripts/handoff_check.py:60-100,150-180,515-600,630-665,1625-1690",
      "ai-packages/qa-factory/agents/qa-code-critic.md:55-100",
      "ai-packages/qa-factory/handoffs/s5-critic-to-automator.yaml",
      "ai-packages/qa-factory/scripts/brief_pack.py:145-173,236-260",
      "ai-packages/qa-factory/scripts/run_suite.py:455-485",
      "ai-packages/qa-factory/scripts/probe_by_code.py:1-40",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/cart-1 (critic forms, run blocks)",
      "ai-packages/qa-factory/scripts/tests/fixtures/stories/local-1-0108/work/handoffs/S5-qa-code-critic-14.yaml",
      "ai-packages/qa-factory/scripts/tests/fixtures/driver-exits/known_red.json"
    ],
    "reruns": [
      {"command": "( cd ai-packages/qa-factory && python -B scratchpad/keep_main.py )  (dry_world.main_pass with World.close not deleting)", "result": "main/stop at S5, 2 findings (receipt_ref, runtime_provenance); main/time 393.5 s; known red main/S5 -> FV3-20; world kept"},
      {"command": "read state/dry-stub.jsonl of the kept world, row S5-qa-code-critic-1", "result": "window_record exit 0, window file and review receipt written; handoff_check --fix exit 1 with both fields blank"},
      {"command": "python -B scratchpad/probe_deriver.py", "result": "_review_receipt -> None with the file present (no header.dispatch, no art.dispatch); control with art.dispatch set -> work/windows/S5-qa-code-critic-1.json; window_runtime_record -> None, no run block of the critic dispatch"}
    ]
  }
}
```
