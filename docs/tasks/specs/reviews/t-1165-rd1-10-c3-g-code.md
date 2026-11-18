# t-1165 — code critic, card C3-g (RD1-10, B-281), builder t-1157, commit de564c68

Spec: `docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` §2 (:121-479), Lead decisions :997-1004 (G-5 = (a)).
Worktree: `C:/QAFactory/forge-repo/.claude/worktrees/agent-a373eda7f9aaf5ac7`, HEAD de564c68 on base 2b2d0f17.

**Verdict: NEEDS WORK — 0 blocking findings, 2 fixes for the same node's fix round (neither blocks the merge), 1 report gap closed by this verdict.**
The decision to accept belongs to the Lead.

## Findings

1. **(fix, does not block the merge) The request-road refusal this card gives a door still arrives with a false-cause sibling line in the managed world.**
   Surface: the refusal text of the baseline request road (`execution_request.validate_request` → `validate_baseline_request` + `validate_managed_gate`).
   `validate_managed_gate` (`baseline_contract.py:103-104`) calls `build_baseline_fields(matches[0], …, request.get("runtime_provenance") or {})`. That call re-runs `validate_baseline_request` and raises `ValueError` on the very revision mismatch item 7 refuses. Then the `except (… ValueError …)` at :117-118 turns it into "managed baseline Gate A state is unreadable".
   Probe (fake `controller` module, real `hooklib.artifact_root`, controller.json + events.jsonl on disk, script `C:/Users/i_mas/AppData/Local/Temp/claude/b3e3188b390a00d9/501cb4e0-b55f-46d8-9262-11b1caefad61/scratchpad/probe_mg.py`):
   ```
   {'expected_source_revision': 'old'} -> [] []
   {'expected_source_revision': 'new'} -> door-line ['managed baseline Gate A state is unreadable']
   ```
   So `RequestError` carries the new door line plus a line that says the state is unreadable, and the conductor may go after the wrong cause (FR-1: a refusal says what is wrong). The same happens for a non-dict truthy `runtime_provenance`. Before this change it was an uncaught `AttributeError`; now it is a caught `ValueError`, so the false line gets that case too.
   This is pre-existing for the revision case, and it sits outside the owns (`validate_managed_gate` is owned for "its reads of baseline_contract only"). But it is in the function the builder edited and in the refusal the card exists for (rule 9, sweep the artifact first; PROJECT.md «Командная работа» п. 9: minor remarks are fixed in the same node's round).
   Recommended fix (Lead widens the owns by this one call): put `build_baseline_fields` in its own `try`. On `ValueError`, return `[]` when `validate_baseline_request(request)` is non-empty, because the caller already holds those named errors. Otherwise return "baseline fields cannot be derived from the current approved plan: <exc>". Add one row to `test_a_malformed_baseline_block_is_named_not_crashed` or item 5's table (managed world, runtime `new` → no "state is unreadable" line).
   If the Lead does not widen the round, the line for «Остатки» is: `validate_managed_gate except masks build_baseline_fields ValueError as "state is unreadable" | узел: <new C3-g fix node, rules-debt/1>`.
2. **(fix, trivial) A comment that lies.** `test_gate_registry.py:1196`: the RD1-27 comment now counts "five sites", but its parenthetical list of site-row files ("test_run_freshness, test_proof_level, test_execution_request, test_controller_state") does not name `test_baseline_contract`, which now carries the fifth site's row. Add it.
3. **(report gap, closed here, no builder round) Axis-5 lines missing.** The DoD says "The report carries the axis-5 lines", one line per hit. The builder ran a narrowed grep instead. I ran the card's own grep (case-insensitive `captured|inconclusive|baseline receipt|approved before revision` over `references/*.md`, `skills/`, `agents/`): **32 hits**. Positive control: the same grep on `references/gate-registry.json` gives 7. Enumeration, all "checked, no edit (meaning unchanged)" because none names a baseline receipt or its `status` word:
   - the manual/run verdict `inconclusive` (pass|fail|inconclusive): artifact-contract-run.md:13,25; coverage-design.md:170; execution-lifecycle.md:98; manual-evidence-app.md:57; manual-evidence.md:76,81,90,91,96,120; walk-charter.md:26; qa-doctor/SKILL.md:241; s6.md:100; s7.md:14,15,37,49; qa-runner.md:23,25; qa-automator.md:86;
   - the generic verb "captured" (a captured file or text): artifact-contract-run.md:76; explore-charter.md:13,104; manual-evidence.md:73,79,113; s6.md:120; s7.md:192,248,249; qa-runner.md:50.
   - Cross-check: of the 32, `grep -iE "baseline|before"` gives 0. A wider `baseline` + `receipt|status|captur` grep over the same scope finds controller-api.md:156 ("a missing before capture is shown at S8, never a blocker"), environment-preparation.md:11 and s6.md:15,130 (dormant). All of them stay true after C3-g: the gap is still non-blocking, and only the reason sentence can differ.
   The Lead takes this enumeration into the acceptance in place of the builder's per-hit lines.

## The builder's gaps the dispatch asked about

- **(a) axis 5**: the negative holds by my own grep (finding 3). There is no prose twin to edit.
- **(b) the early return on a non-dict `baseline_contract`**: the card is NOT silent here. Item 8 says "append … and return the errors collected so far, together with the runtime line below if that applies. The key checks are skipped". The "runtime line" is item 8's own non-dict runtime sentence, which goes in place of the revision line. The builder computes it before the return (:23-28). The revision line cannot be built without a readable `baseline_revision`.
  Direction: always a refusal (errors are non-empty), never a pass and never a crash.
  Probe: `'x'` + dict runtime → 1 named error; `[]` + `5` → both named errors; `False` → named. E14's "None, absent and {} keep today's errors" holds (the `{}`/False-runtime probe gives the full "requires …" list). **Judged: as specified, safe.**
- **(c) `WHY_RECEIPT_UNJUDGED` + `registry_why(problem, tail)`**: `gate_template.registry_why` exists on the base (`gate_template.py:63`), so the family form is the one G-5 = (a) chose. The constant equals item 3's text, and `problem` is read once per call (:210). The reason is used only when `problem and matching` (:244), exactly E2's condition. The RD1-27 row was added with the expected bytes. **Judged: as specified.**

## Standing questions (critic.md rule 22)

- **Q1 fit to the spec**: met; finding 1 is a neighbour, not a miss of the card.
  - Item 1: the row matches word for word (vocabulary, field, words, verdict_map, accepts, the two produce sites, decides, status, debt_ref); unchanged keys untouched.
  - Item 2: `matching`/`candidates` (:215-225), equalities unchanged and in order, lazy import.
  - Item 3: as above.
  - Item 7: the text matches the spec byte for byte, appended after the kept prefix under the unchanged condition.
  - Item 8: both messages verbatim; `validate_managed_gate` reads `bcontract` at the three sites.
  - E1-E14 traced, nothing violated: E4 (the predicate is applied after the equalities, revision/hash loop unchanged); E10 (`acceptable` errs only to False); E11 (`ready`/`blocks_execution` untouched); E12 (one reader, below); E13 (falsy non-dict contract/runtime were refused before and are refused now; no request accepted before is refused now).
- **Q2 the builder's own decisions**: the order of errors (the runtime-shape line before the contract "requires" lines) is unstated in the card and harmless. No other silent point.
- **Q3 seams**: additive. C3-g2 and C3-k3 follow on the same two files, and the edits are localized to the owned functions and the `baseline_identity` pins. The F1/NEG lines were renamed in place, as E9 asks.
- **Q4 class-wide completeness**: covered.
  - axis 5: covered (finding 3);
  - the second producer: registered;
  - `manual_evidence.validate_baseline_record:668/:674` (it still crashes at :674 on a truthy non-dict contract, after the request check now returns named errors): G-8 → C3-k3, already queued;
  - the `delivery_summary`/`controller` analogs: C3-g2, queued;
  - the managed-gate false cause: finding 1.
- **Q5 tests**:
  - (a) killing power: the registry rows are red before (old code counts `captured` under a broken registry, and the `inconclusive` row gets "missing"); item 5's door substrings are red before; item 8's `"old"` runtime and managed-gate `"x"` rows were `AttributeError` before; the `captured` control row turns red on a consumer typo (E3).
  - (b) every expected value comes from the card's items 4/5/8.
  - (c) every new door has a row.
  - (d) no existing method was edited.
  - (e) no duplicates found.
  - (f) the `tests-over:` line is present, and its reason holds: three tables, each the card's.
  - (g) no new file; `test_baseline_contract.py` is `gate_named` in test-layers.json:213 and ran in 0.043 s.
- **Q6 duplication and consistency**: none found. The status word goes through the one predicate `gate_template.acceptable`, and the registry sentence through the one builder `registry_why` (other users: proof_level.py:984/1641, execution_request.py:2108, controller.py:5585). The "must be a JSON object, got <type>" shape refusals are inline per module across the package (adapter_forms.py:189, assertion_detectors.py:219/304); there is no shared helper to reuse. The clone ratchet is the canon's.
- **Q7 code quality**: no function over 60 new lines and no deep nesting. Cosmetic only: the continuation lines of `matching = [` (:216-224) keep the old `candidates = [` alignment, 2 columns off. This is not a finding. The lying comment is finding 2.
- **Q8 hygiene**: CRLF kept (the CR counts follow the line counts: 248/265/737). Cyrillic in the package diff: 0.
- **Q9 ratchets**: `D13_ITEM_COUNT` 150 → 151, named in its comment with the triple (`manual_evidence.py`, `write_baseline_receipt`, `baseline_identity`). I re-measured it: `GR.analyse` gives 151 items, and `--sites` shows the one new line `manual_evidence.py:728 … [baseline_identity]` with no `baseline_contract.py` line. That is the spec's measurement exactly. No other ratchet was touched.
- **Q10 architecture**: AR-9/12/13/16/19/20/22/28/29 are named and kept. AR-22: `provenance\.baseline` gives 0 hits (control `provenance\.environment_preparation` gives 4), and the new consumer has its reader at :225.
- **Q11 judgment**: `judgment: none` holds: a membership join and shape refusals. No census or scan-constant edits.
- **Q12 one road**: none found. One reader of the receipt word (grep of `["']captured["']|["']inconclusive["']` over `scripts/*.py`: producer `baseline_contract.py:155`, producer `manual_evidence.py:728`, the shape check `:668` (C3-k3)). No language, project or case branch.

## Spot-checks (claims re-run)
- `test_baseline_contract`: "Ran 10 tests … OK" (matches the builder).
- `gate_registry.py --check`: exit 0, "3 gate(s) left as debt:" (stand_identity, provenance_acceptance, s5_stand_limits), with no `baseline_identity`.
- `refusal_registry.py --check`: "A24 refusal registry: no violations", exit 0.
- The `provenance.baseline` grep: 0 (control 4).
- D13: 151.
- Not re-run: `test_gate_registry.py` (slow; the batch canon judges it, and the builder reports 505/505).

## Trail
- Read:
  - the spec §2 :100-499 and :985-1013;
  - critic.md :150-299 (rules 18-24);
  - `git show de564c68` (all 5 files);
  - `baseline_contract.py` :1-140 and :193-250 (worktree);
  - `gate_template.py` :1-110;
  - `manual_evidence.py` :655-700;
  - `execution_request.py` :119-130;
  - `delivery_summary.py` :148-180;
  - `test_gate_registry.py` :1196-1210;
  - `test-layers.json` :213-221 and :2033-2040.
- Commands: as in the json block below, plus the CRLF/Cyrillic counts and the `"must be a JSON object"` grep.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "axis 5 prose twins: 32 hits of the card grep, none names a baseline receipt or its status word (control gate-registry.json 7) - no edit; second producer registered; validate_baseline_record crash -> C3-k3 (G-8); delivery_summary/controller analogs -> C3-g2; new neighbour: validate_managed_gate except masks build_baseline_fields ValueError as 'state is unreadable' beside the new door line (finding 1)",
  "fixes": [
    "baseline_contract.py:103-118 validate_managed_gate: a revision-mismatch or non-dict runtime makes build_baseline_fields raise ValueError, reported as 'managed baseline Gate A state is unreadable' beside the door line (probed); own try around the call, [] when validate_baseline_request already refused, else a named 'cannot be derived from the current approved plan' line; one test row; needs the Lead to widen owns by this call, else a node line in Ostatki - does not block the merge",
    "test_gate_registry.py:1196 RD1-27 comment says five sites but its site-row file list omits test_baseline_contract - add it (trivial)",
    "report: the axis-5 per-hit lines are missing from the builder report; the critic's enumeration in this file stands in, Lead attaches it at acceptance (no builder round)"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md:100-499,985-1013",
      ".claude/agents/critic.md:150-299",
      "git show de564c68 (5 files)",
      "worktree ai-packages/qa-factory/scripts/baseline_contract.py:1-140,193-250",
      "worktree ai-packages/qa-factory/scripts/gate_template.py:1-110",
      "worktree ai-packages/qa-factory/scripts/manual_evidence.py:655-700",
      "worktree ai-packages/qa-factory/scripts/execution_request.py:119-130",
      "worktree ai-packages/qa-factory/scripts/delivery_summary.py:148-180",
      "worktree ai-packages/qa-factory/scripts/tests/test_gate_registry.py:1196-1210",
      "worktree ai-packages/qa-factory/scripts/tests/test-layers.json:213-221,2033-2040"
    ],
    "reruns": [
      {"command": "python -B <wt>/scripts/tests/test_baseline_contract.py", "result": "Ran 10 tests in 0.043s OK"},
      {"command": "python -B <wt>/scripts/gate_registry.py --check", "result": "exit 0; A26 gate registry: no violations; 3 gate(s) left as debt: stand_identity, provenance_acceptance, s5_stand_limits"},
      {"command": "python -B <wt>/scripts/gate_registry.py --sites | grep baseline_contract.py|manual_evidence.py:7xx", "result": "manual_evidence.py:728  write_baseline_receipt  record['capture_status'] == 'captured'  [baseline_identity]; no baseline_contract.py line"},
      {"command": "python -B <wt>/scripts/refusal_registry.py --check", "result": "A24 refusal registry: no violations; exit 0"},
      {"command": "grep -rniE provenance\\.baseline <wt> | wc -l ; control provenance\\.environment_preparation", "result": "0 ; 4"},
      {"command": "GR.analyse(GR.PLUGIN_ROOT) len(items)", "result": "151"},
      {"command": "axis-5 grep -rniE captured|inconclusive|baseline receipt|approved before revision over references/*.md skills agents ; control gate-registry.json", "result": "32 hits, 0 mention baseline/before ; control 7"},
      {"command": "python -B scratchpad/probe_mg.py <wt>/scripts (validate_managed_gate, fake controller, runtime old/new)", "result": "old -> [] ; new -> door-line + ['managed baseline Gate A state is unreadable']"},
      {"command": "validate_baseline_request probes: contract 'x' / [] + runtime 5 / False / {} + runtime False", "result": "named contract error only; both named errors; named bool; runtime-bool line + the full requires list"}
    ]
  }
}
```
