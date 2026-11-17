# Rules-debt wave 3, round 2: cards C3-g, C3-g2 (baseline_identity) and C3-h (stand_identity) (t-1097, F19, node rules-debt/1/RD1-10)

Designer draft for the Lead. This file REPLACES `docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards.md` (t-1085) for the
builder: a builder reads this file and not the old one. It applies every remark of the plan critic t-1090
(`docs/tasks/specs/reviews/t-1090-rules-debt-wave3-g-h-plan.md`, G1-G7 and H1-H5) and the Lead's changed decisions of
17.11.2026. The closing table «Remarks -> where applied» maps each remark to its place.

Parent spec, unchanged and not edited: `docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md`. Its shared items S-a..S-f
(:278-346), the E-c table (:372-402) and the Lead decisions (:1873-1893, :2161-2183, :2294-2348) apply to every card here.

The owner's word, 17.11.2026, as the Lead relays it: a remark of a critic or of a card is FIXED in its round. It is never filed
as a finding that grows the rules debt. So no card in this file files a finding.

Where facts were read (17.11.2026):
- main, the root checkout `C:/QAFactory/forge-repo`;
- the worktree `C:/QAFactory/forge-repo/.claude/worktrees/agent-ac40b44fb0a175afa/` (called «the C3-b2 worktree» below). It holds
  C3-b2, C3-d and C3-reg-precondition, which main does not hold yet, and the RD1-27 builder function
  `gate_template.registry_why`.

Nothing was RUN by this designer. Every command below is for a builder or the Lead. Every count of a pin is «by measurement at
the build», never estimated here.

## §0. State the cards are based on (read today)

1. **The family builder of the «registry cannot be read» text exists on the C3-b2 worktree only.**
   - `gate_template.registry_why(reason, tail, *, stop=False)` is at the C3-b2 worktree's `scripts/gate_template.py:60-68`.
     - With `stop=False` it returns `"the gate registry cannot be read ({reason}): a factory defect, {tail}"`. That is the
       in-line form, for a site that judges a reuse.
     - With `stop=True` it returns `"gate registry unreadable: the plugin's references/gate-registry.json cannot be read
       ({reason}). {tail}"`. That is the dispatch stop's opening.
   - Its callers on that worktree are `controller.py:5560-5564` (the stop), `execution_request.py:2108`, and
     `proof_level.py:984, :1641`.
   - The test table `test_gate_registry.py:1188-1199` («RD1-27: the four sites ... take ONE builder») pins all four.
   - The same Grep pattern on main's `scripts/` gives 0 hits. The worktree hits are the positive control.
2. **Pins on the C3-b2 worktree.** These are informational only. The builder measures on its own base.
   - The debt block is 4 rows (`test_gate_registry.py:63-65`: `stand_identity`, `provenance_acceptance`, `baseline_identity`,
     `s5_stand_limits`).
   - `"4 gate(s) left as debt:"` (:256), and the split `{"converted": 23, "debt": 4, "exempt": 6}` (:355).
   - `D13_ITEM_COUNT = 150` (:1069).
   - The F1 baseline check is labelled «F1 provenance.baseline lives under baseline_identity» (:651), and the F1 loop is at
     :660.
   - K-N2.12 NEG is :295-302.
3. **Test files.**
   - `test_baseline_contract.py` is a keep row (`test-layers.json:213`, layer `gate_named`). It is fast: it is not in
     `slow_tests.json` (t-1085 §0.4 grep, with a positive control).
   - `test_gate_registry.py` (19.7 s), `test_stand_identity.py` (27.4 s) and `test_story_run_stand_identity.py` (205.7 s) are
     slow, and the batch canon judges them (`plans/builder-rules.md:50-53`).
   - `test_handoff_producers.py` and `test_human_reading.py` are QUARANTINED (`test-layers.json:8493`, `:8583`, cohort
     entries). No row goes there.
4. **The baseline machinery is dormant for roles.**
   - `skills/qa-story/phases/s6.md:130` says "The baseline machinery below stays dormant: no role captures
     `evidence_phase=baseline` now".
   - `references/role-commands.json` lists no baseline command for any role. A case-insensitive Grep for `baseline` gives 0
     hits; the same file holds `manual_evidence.py prepare` and the other entries, read at :1-30.
   - The judgment census gives every baseline unit to `"roles": ["conductor"]` (`judgment-census.json:43-47`, `:232`).
   - The conductor's skill names the controller operations (`s5.md:379`, `s6.md:142`: `controller.py --task-root <TASK_ROOT>
     --operation deployment-inputs`).
   - `controller.py:10045-10048` serves `baseline-inputs` and `deployment-inputs`.

## §1. Architecture, rules, owners (designer rule 1)

**FR walk** (the sections touched, per card):

| card | A refusals | B text to a person | C contracts | D identity | E delivery | G code |
|---|---|---|---|---|---|---|
| C3-g | FR-1, FR-2, FR-4, FR-57 (item 7: the door of the revision refusal; item 8: non-dict named) | FR-3, FR-6 (item 3: the gap reason reaches `delivery_summary.render`'s «Before/after comparisons» block, `delivery_summary.py:569-574`; G4) | FR-13 (the words are data), FR-14 (the gap dict keeps its keys) | FR-59 (an unreadable registry never counts) | FR-41 (never "missing" for an unjudged receipt) | FR-30, FR-32 |
| C3-g2 | FR-1 (an unreadable receipt is named by what was expected) | FR-6 (the new reason reaches the same block) | FR-14 (no key added) | FR-59 | FR-41 (the core of the card) | FR-30, FR-32 |
| C3-h | none (no refusal moves) | none (no text changes) | FR-13 | FR-59, FR-40 (the unaskable unknown takes its declared safe default) | none | FR-30 |

F (measurement) is untouched by every card.

**AR-n and the change check each one demands.** Each check is also written into the card's DoD.
- AR-9 (`architecture.md:106-111`), C3-g items 7-8:
  - Change check: "a new refusal arrives in one commit with its A24 row, its door and its person's-word route. Regenerate
    controller-blocks.md, then run both detectors."
  - The DoD runs `refusal_registry.py --check` before and after. `controller-blocks.md` is untouched: `tools/controller-blocks-gen.py:22`
    reads only `scripts/controller.py`, and C3-g edits no controller raise.
  - The person's-word route: the refused party is the conductor (§0.4). The person's route is S8's question of where to get
    before evidence (`s5.md:387-389`), and missing before evidence blocks nothing (`s5.md:377`). No word passes the old-build
    identity (`promotable: false`, P27).
- AR-12 (:127-132), C3-g items 7-8: a change to a validator a role calls names the roles it affects. No role calls it (§0.4),
  so the commit says "code_friction: not measured -- dormant for roles (s6.md:130)".
- AR-13 (:161-166):
  - C3-g: the receipt's word is read only through `gate_template.acceptable`.
  - C3-g2: the receipt FILES are read through `hooklib.read_json` (axis 16), at one new reader.
- AR-15 (:176-180), C3-g2: two callers read the receipt folder two ways (one crashes, one skips silently), and get one survivor,
  `baseline_contract.load_receipts`.
- AR-16, C3-g item 3: the text uses the family's one builder `registry_why` when the base has it (§0.1; fork G-5).
- AR-19 (:204-208), C3-g: axis 5 prose twins are walked by grep, because the row's words change. C3-h: no word changes.
- AR-20 (:220-224): every pin moves by a named delta, measured.
- AR-22 (:236-240):
  - C3-g: the consumer `baseline_identity.readiness` lands with its reader, and the readerless `provenance.baseline` leaves.
    The name is grepped over the package.
  - F-k4 (b): C3-k3 adds `baseline_identity.capture` BESIDE it.
- AR-28 (:278-282): every new gate read's behaviour on missing, unreadable and empty input is stated and pinned (C3-g items 4,
  5, 8; C3-g2 item 4). C3-h E1 is restated per H1.
- AR-29 (:134-157): the class and owner of every check, in the table below. Change check: run `test_judgment_census.py`
  (printed by `--witness-for`); a raised count is named in the verdict.

**Checks added or altered, their owner and census class:**

| check | card | owner it serves | census class | blocking |
|---|---|---|---|---|
| `deployment_readiness`: is the receipt's `status` a word the consumer `baseline_identity.readiness` takes (`gate_template.acceptable`) | C3-g | data (a join of a producer's word to its registry row) | no unit (`judgment-census.json` has no `deployment_readiness` row; rows :42-47 are the positive control); xref in kind | no (`blocks_execution: False`, `ready: True`) |
| the gap reason when the registry cannot be read | C3-g | data | no unit (a string in an appended dict) | no |
| `validate_baseline_request`: the revision refusal now names its door | C3-g | data | unit unchanged: `shape`, owner data (`judgment-census.json:45`) | yes, as today |
| `validate_baseline_request`: a non-dict `baseline_contract` / `runtime_provenance` is refused by name | C3-g | data | the same unit, `shape` | yes (it was a crash, which also stopped; now a named refusal) |
| `validate_managed_gate`: a non-dict `baseline_contract` reads as an empty contract, never a crash | C3-g | data | unit unchanged: `xref` (`judgment-census.json:46`) | yes, as today (it refuses; never passes) |
| `load_receipts`: a receipt file that is not one readable JSON object is counted as unread | C3-g2 | data (presence and shape of a file) | no unit: it raises nothing and its name matches no unit pattern (`UNIT_NAME_RE`, `test_judgment_census.py:77`) | no |
| `deployment_readiness`: an unread receipt makes the gap reason "not known", never "missing" | C3-g2 | data | no unit | no |
| `stand_identity` row: `vocabulary` target -> code, status converted | C3-h | data | none (registry rows are not census units) | unchanged |

**Commit lines.**
- Each card gives its `architecture:` and `judgment:` lines as CONTENT. Their form has ONE carrier, `tools/architecture_gate.py`;
  this draft does not copy its grammar.
- `judgment: none` always carries its ` -- <why>`.
- `tests-over:` has its carrier in `tools/test_volume.py`.

---

## §2. Card C3-g — baseline_identity through the predicate, with its door (B-281) — wave 3

**Facts (read today; t-1085 facts that stand are kept, re-read where marked).**

- **The refusing site (S-b).** `baseline_contract.validate_baseline_request` (`baseline_contract.py:8-30`, the row's `validate`
  site) is the site.
  - It compares `runtime_provenance.expected_source_revision` with the contract's `baseline_revision` (:21-23). It appends
    "baseline runtime must match the approved before revision", and that sentence names no door.
  - It returns an error list. Its callers turn the list into a refusal:
    - `build_baseline_fields` raises `ValueError` (:50-52);
    - `baseline_receipt` raises (:114-116);
    - `execution_request.validate_request` collects the list (:124-125) and raises `RequestError`;
    - `manual_evidence.validate_baseline_record` collects it (:673), and `write_baseline_receipt` raises (:713-715).
- **Who builds a baseline request (G-2, FR-2).** Read today:
  - `Controller.baseline_inputs` (`controller.py:2239-2250`) is served as `controller.py --task-root <T> --operation
    baseline-inputs --input <options.json>` (:10045-10046). It takes `plan_row` and `runtime_provenance` from the options file
    and calls `build_baseline_fields`.
  - The run road (`run_suite.py:2393-2394` -> `write_baseline_receipt`) and the manual road (`manual_evidence.py:2239`) take a
    request or record that already carries that block.
  - No role is told to build one (§0.4). The refused party is the conductor, and `controller.py` operations are in the
    conductor's set (`s5.md:379`).
  - So a door in that party's set exists. It is (i) build the request again through `baseline-inputs` with the record of a
    probe that read the before build, or (ii) capture no baseline: missing before evidence is an `awaiting_baseline` gap and
    blocks no current check (`s5.md:370-377`, `deployment_readiness` docstring :176-182).
  - No owner decision is needed to name it, so no fork is returned for it.
- **Non-dict input (G-3).**
  - `request.get("baseline_contract") or {}` (:14) and `(request.get("runtime_provenance") or {}).get(...)` (:21) raise
    `AttributeError` on a truthy non-dict.
  - The same class sits in `validate_managed_gate` (:77, :86, :93: `request.get("baseline_contract", {}).get(...)`). It is the
    next call on the same road (`execution_request.py:126-127`), and its `except` (:96) does not catch `AttributeError`.
  - Fixing :14/:21 alone leaves `validate_request` crashing one call later, so the sweep of this file (CLAUDE.md rule 9, sweep
    the artifact first) puts both in this card.
- **The accept site.**
  - `deployment_readiness` (:175-221) never refuses. A receipt counts when the equalities hold (:189-198) and `r.get("status") ==
    "captured"` (:199), then when the source revision and evidence hashes hold (:201-214).
  - Otherwise the row gets the gap `awaiting_baseline`, `blocks_execution: False`, reason "baseline evidence missing, stale or
    incomparable" (:216-218).
  - The reason reaches a person: `delivery_summary._comparison_readiness` keeps it (:172-177), `build` puts it in
    `comparison_gaps` (:415), and `render` prints `- <case>: <reason>` under «Before/after comparisons awaiting a before-state
    capture» (:569-574).
- **The words.** They live in the receipt's `status`. There are two producers:
  - `baseline_receipt:134` (`"captured" if captured else "inconclusive"`);
  - `manual_evidence.write_baseline_receipt:718` (`record["capture_status"]`, shape-checked at :668).

  There is one reader, `deployment_readiness:199` (critic t-1090 reproduced: grep `["']captured["']|["']inconclusive["']` over
  `scripts/*.py`).
- **The consumer `provenance.baseline` is read by no script.** The package-wide case-insensitive grep finds only the registry and
  `test_gate_registry.py`. The positive control `provenance\.environment_preparation` gives 4 hits (t-1090 rerun).
- **The premise "the predicate equals today's literal".** The critic RAN it: 10/10 values equal, True only on `captured`. A
  broken registry gives False (t-1090 facts table, `d13.py`).
- **There is no recorded data.** No fixture holds a baseline receipt (t-1085 §2, Glob and grep with controls), so the control is
  item 4's table.
- **F-T3 is recorded.** G-0 = (a) (Lead, 17.11.2026). **F-k4 = (b)** (Lead, 17.11.2026): C3-g owns the consumer move, and C3-k3
  only adds `baseline_identity.capture`.

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/human-questions.md` (:1-63)
- this card, and the C3 shared items S-a..S-f of `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:278-346)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
  - `scripts/baseline_contract.py` (whole, 222 lines)
  - `scripts/gate_template.py` (whole; on the base, check for `registry_why`)
  - `scripts/manual_evidence.py:658-737`
  - `scripts/execution_request.py:119-128`
  - `scripts/controller.py:2239-2263`
  - `scripts/delivery_summary.py:148-179, 565-574`
  - `scripts/gate_registry.py:21-45, 485-681, 786-912`
  - `references/gate-registry.json` (row `baseline_identity`)
  - `scripts/tests/test_baseline_contract.py` (whole)
  - `scripts/tests/test_live_audit_contract.py:38-57`
  - `scripts/tests/test_gate_registry.py`: the debt/converted pins, K-T1.2, the split, K-T1.14, F4 `code` list, K-N2.12 NEG (grep `provenance.baseline`), F1 (`part_fix_pass`), D13, the C3-0 seam (grep `GT._READ`), the RD1-27 table (grep `RD1-27`) if present
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `baseline_identity` only: `decides`, `sites`, `field`, `words`, `verdict_map`, `accepts`, `vocabulary`, `status`, `debt_ref`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py` (`validate_baseline_request`; `validate_managed_gate`, its reads of `baseline_contract` only; `deployment_readiness` with its point-of-use import; one module constant for the registry-why tail)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` (new parameterised methods of items 4, 5, 8; no existing method edited)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (the S-f pins of `baseline_identity`; the F1 `baseline_identity` lines; K-N2.12 NEG; one RD1-27 row if that table is on the base)
non-goals:
- `build_baseline_fields`, `baseline_receipt`, `write_baseline_receipt` code (they re-raise the list; their text follows item 7 with no edit)
- `deployment_readiness`'s handling of a non-dict receipt and both callers' receipt reading: that is C3-g2, after this card
- `manual_evidence.py` code (registry sites only, item 1): `validate_baseline_record` is C3-k3's (fork G-8)
- `execution_request.py`, `profile_contract.py`, the `provenance.*` consumers (C3-k)
- `controller.py`, `delivery_summary.py` (C3-g2)
- `gate_template.py`, `gate_registry.py`, `judgment-census.json` (no unit moves)
- `docs/SIBLING_MAP.md`; any new test FILE; any finding file
handoff: report path given by the Lead
edges: E1-E14 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0; `baseline_identity` is absent from the `N gate(s) left as debt:` block; no F-b names `deployment_readiness`. `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/refusal_registry.py --check` exits 0 before and after (AR-9). The case-insensitive grep `provenance\.baseline` over `C:/QAFactory/forge-repo/ai-packages/qa-factory/` gives 0 hits after (AR-22; positive control `provenance\.environment_preparation` > 0). Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and every printed non-slow file, at least `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py`. `test_gate_registry.py` is slow: the batch canon judges it, and the report names it. The report carries the axis-5 lines (siblings), the D13 before/after measurement, and the line "code_friction: not measured -- dormant for roles (s6.md:130)" (AR-12).
siblings:
- axis 5 (`docs/SIBLING_MAP.md:143`, gate rows <-> sites <-> prose twins): the row's words change.
  - The builder greps case-insensitively for `captured|inconclusive|baseline receipt|approved before revision` over `references/*.md`, `skills/` and `agents/`.
  - The positive control is the same grep finding `references/gate-registry.json` when `references/*.json` is included.
  - Each hit gets a report line, "checked, no edit (meaning unchanged)" or the edit made. The critic's grep found no twin.
- the second producer of the word, `manual_evidence.write_baseline_receipt`: registered (item 1, G-1 (a)).
- the shape check `manual_evidence.validate_baseline_record:668`: a `provenance_acceptance` site, owned by C3-k3. Its non-dict crash and its doorless sibling sentence (:689) are fork G-8, with the edit text for k3.
- the two analogs of G1 (`delivery_summary.py:156-162` skips an unreadable receipt; `controller.deployment_inputs:2258-2259` crashes on a non-dict or non-JSON receipt): card C3-g2 in this file.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` (C3-g)

Items:
1. **Registry row `baseline_identity`** (F-T3 (a), G-0 (a), G-1 (a)):
   - `vocabulary: "code"`, `field: "status"`, `words: ["captured", "inconclusive"]`;
   - `verdict_map: {"captured": {"class": "matched"}, "inconclusive": {"class": "unknown", "owner": "environment"}}`;
   - `accepts: {"baseline_identity.readiness": ["matched"]}`. `provenance.baseline` is REMOVED in this commit (AR-22; F-k4
     (b)). C3-k3 later adds `baseline_identity.capture` under `provenance_acceptance`, beside this consumer (E9);
   - unchanged: `promotable: false`, `unknown_branch: refuse_with_door`, `refuse_with_door`, `waits_at: null`, `closed_by`,
     `addressee`, `person_subject`;
   - sites:
     - `validate_baseline_request` stays `validate`;
     - `deployment_readiness` stays `accept`;
     - added: `{"file": "baseline_contract.py", "function": "baseline_receipt", "role": "produce"}`;
     - added: `{"file": "manual_evidence.py", "function": "write_baseline_receipt", "role": "produce"}`;
   - `decides`: "the before-state evidence was captured on the approved old build: a request whose runtime does not name the
     approved before revision is refused with its door (validate_baseline_request), and a receipt counts as before-evidence
     only when its status is `captured` and its identity, gate and evidence hashes match; `inconclusive`, any other word or none
     leaves an awaiting_baseline gap, never a pass (identity on the OLD build stays code-proven: a person's word never stands in
     for it)";
   - `status: "converted"`, `debt_ref: ""`.
2. **`deployment_readiness`, the acceptance, ONE conjunct list (G5).** The comprehension :189-199 becomes two lists:
   - `matching = [r for r in receipts if <the equalities of :189-198, unchanged and in their order>]`;
   - `candidates = [r for r in matching if acceptable(r, "baseline_identity.readiness")]`.

   The loop over `candidates` (:200-214) is unchanged. Nothing else reads the conjuncts: no second copy of the list exists (the
   clone ratchet counts one). The import is `from gate_template import acceptable, registry_problem` inside the function, plus
   `registry_why` when the base has it (item 3). This is the file's lazy style (:64, :71). Expected from F-T3 (a), C3-0 E9 (one
   road), and the row's `decides`.
3. **The gap reason when the registry cannot be read** (F-T11 (a); G4, G5; family text):
   - Read `problem = registry_problem()` once per call.
   - When `problem` is non-empty AND `matching` is non-empty for the row, the gap's `reason` is the family's in-line sentence:
     - `registry_why(problem, WHY_RECEIPT_UNJUDGED)` (stop form False) when the base's `gate_template` defines `registry_why`
       (§0.1);
     - otherwise the same bytes written in place: `f"the gate registry cannot be read ({problem}): a factory defect,
       {WHY_RECEIPT_UNJUDGED}"`;
     - with `WHY_RECEIPT_UNJUDGED = "the baseline receipt was not judged"`, one module constant.
   - Every other gap keeps "baseline evidence missing, stale or incomparable".
   - The gap dict keeps its keys (FR-14).

   This holds for every receipt in `matching`, whatever its word: a broken registry with an `inconclusive` receipt also gets the
   registry reason. That is true, because the word was not judged (G5).

   Which of the two family forms is used is fork G-5. The card executes on the recommendation, the in-line form.
   - FR-3: the defect is reported, never asked.
   - FR-6: the sentence is a status line of the «Before/after comparisons» block, which already ends in the S8 question
     (`delivery_summary.py:574`). It names no path inside the plugin, no JSON record, no script and no dispatch id
     (`human-questions.md:42-62`).
   - `<problem>` is `load_registry`'s own short sentence, the same as at the family's other sites. Whether a factory word
     ("gate registry") may stand in that line is part of fork G-5.

   Expected from FR-41, FR-59 and FR-3.
4. **Test, the acceptance table** (S-b, accept side). One new parameterised method in `test_baseline_contract.py`, for example
   `test_a_receipt_counts_only_by_its_accepted_status_word`, with a `subTest` per row.
   - The world is the receipt and plan row of `test_runner_receipt_is_captured_not_product_pass_and_detects_stale_binding`
     (:24-39), with the evidence file hashing as recorded.
   - Each row expects (`comparisons_ready`, gap reason). `ready` is True and `blocks_execution` False in every row.

   Rows:
   - `captured` -> (True, no gap). This is the control row; it turns red on a consumer-id typo (E3).
   - `inconclusive` -> (False, "baseline evidence missing, stale or incomparable"). This is the S-b pin of the row's unknown
     word: the declared safe default, a gap and never a count (G6).
   - `Captured`, `" captured"`, `""`, None, `5`, `["captured"]`, no `status` key -> (False, the same reason) each.
   - `captured`, but `source_revision` differs from the row's `baseline_revision` -> (False, the same reason). The predicate is
     never the only guard (E4).
   - Unreadable registry with `captured` -> (False, a reason that starts "the gate registry cannot be read (", contains
     "baseline receipt was not judged", and does not contain "missing").
   - Unreadable registry with `inconclusive` -> (False, the same registry reason) (G5).
   - Unreadable registry with NO receipt -> (False, "baseline evidence missing, stale or incomparable"). A missing receipt is
     still missing.
   - Unreadable registry with a receipt for another `case_version` -> (False, "baseline evidence missing, stale or
     incomparable"). It is not in `matching`.

   The seam:
   - Save `list(GT._READ)`, set `GT._READ[:] = [({"rows": "x"}, GR.structural_error({"rows": "x"}))]`, and restore in
     `finally`. That is the C3-0 precedent (`test_gate_registry.py`, grep `GT._READ`).
   - If the base's `gate_template` names its cache otherwise, use that name. If it exposes none, stop with a question.

   Expected from the row's `decides` (item 1), FR-59, FR-41 and `gate_template`'s error direction. They never come from
   `deployment_readiness`'s output before the change.
   - The registry rows are red before the change, because today's code counts the receipt (t-1090 rerun).
   - The word rows are green before and after. They are the behaviour-preservation control.
   - The existing methods :24-78 stay unedited.
5. **Test, the refusal of an unknown old-build identity, with its accepting control** (S-b, refusing side; G3). One new
   parameterised method, for example `test_an_unknown_old_build_is_refused_never_taken`.

   Inputs:
   - The request for `validate_baseline_request` is `{"evidence_phase": "baseline", "baseline_contract": contract(),
     "runtime_provenance": <row>}`, with `contract()` from :14-20.
   - The row for `build_baseline_fields(row, "gate-A", <row>)` is the approved-row shape of
     `test_builder_binds_approved_row_gate_and_old_runtime` (:118-121). It carries `baseline_reason`; `contract()` does not, and
     passing it would add a "requires reason" error.

   Rows (`runtime_provenance` -> expectation):
   - `{}`, `{"expected_source_revision": None}`, `{"expected_source_revision": ""}` and `{"expected_source_revision": "new"}`:
     the errors contain one that starts "baseline runtime must match the approved before revision" and contains `'old'` and
     `baseline-inputs` (item 7's door). `build_baseline_fields` raises `ValueError` whose text holds the same.
   - `{"expected_source_revision": "old"}` (ACCEPTING control): no error starts with that sentence, and `build_baseline_fields`
     returns without raising. This row is the test that OPENS the door (FR-2).
   - The contract's `baseline_revision` absent AND the runtime's absent: still refused, by "baseline_contract requires
     baseline_revision" (:17-18).

   Expected from the row's `decides` and `unknown_branch: refuse_with_door`. It is red before the change only on the door
   substrings.
6. **S-f pins.** These are deltas from the main the node is based on, measured at the build (§0.2 shows what the C3-b2 worktree
   holds today).
   - `EXPECTED_DEBT` loses `baseline_identity` and `EXPECTED_CONVERTED` gains it, with an AR-20 comment line naming C3-g and its
     task.
   - K-T1.2 `"N gate(s) left as debt:"` becomes N-1.
   - The split: converted +1 and debt -1, with its comment. The K-T1.14 label words that name a count change in the same line.
   - The F4 `code` list gains `baseline_identity`.
   - F1 (`part_fix_pass`):
     - the check «F1 provenance.baseline lives under baseline_identity» becomes `home["baseline_identity.readiness"] ==
       "baseline_identity"`, labelled «F1 baseline_identity.readiness lives under baseline_identity»;
     - the loop pair `("provenance.baseline", "baseline_identity")` becomes `("baseline_identity.readiness",
       "baseline_identity")`. Expect exactly one finding naming the consumer and the row. The critic ran it: exactly one finding
       naming `baseline_identity.promotable`, the consumer and the token.
   - K-N2.12 NEG appends `person_confirmed` to `accepts["baseline_identity.readiness"]` and keeps its expectations: exactly one
     finding, naming the consumer and the word. Its labels name the new id.
   - D13: re-measure with `GR.analyse(PLUGIN_ROOT)` before and after, on the triple set and `len(items)`.
     - Expected (critic t-1090 ran it on main): +1 triple `("manual_evidence.py", "write_baseline_receipt",
       "baseline_identity")` and +1 item, exactly `record['capture_status'] == 'captured'` (`manual_evidence.py:728`).
     - Nothing else moves: `:199` leaves with the code edit, and `baseline_receipt:134` is an IfExp inside a dict value.
     - A different measurement is a stop and a question. The comment line keeps the form of the D13 comment above
       `D13_ITEM_COUNT`.
   - The RD1-27 table («the four sites ... take ONE builder»), only if it is on the base: add the row
     `("baseline_contract deployment_readiness", GT.registry_why("R", B.WHY_RECEIPT_UNJUDGED), "the gate registry cannot be read
     (R): a factory defect, the baseline receipt was not judged")`, and update the comment's count word by measurement. If the
     table is absent, add nothing.

   Expected from the status rule (one row moves debt -> converted) and the comparisons above.
7. **The door of the revision refusal (G-2, FR-1/FR-2, AR-9).** In `validate_baseline_request`, the appended text becomes:

   ```
   baseline runtime must match the approved before revision: runtime_provenance.expected_source_revision is {expected!r}, the approved baseline_revision is {revision!r}. Probe a stand that runs that revision and build the request again with the probe's record as runtime_provenance (`controller.py --task-root <TASK_ROOT> --operation baseline-inputs`), or capture no baseline: missing before evidence is an awaiting_baseline gap and blocks no current check
   ```

   Here `{expected!r}` is the value read (None when absent), and `{revision!r}` is `contract.get("baseline_revision")`.
   - The existing first clause is kept as the PREFIX, so a reader matching the old sentence still matches.
   - Pinned greps on main: "approved before revision" appears only in `baseline_contract.py:23`. The search's positive control
     is that same hit; it found the manual sibling `manual_evidence.py:689` too.
   - The condition is unchanged: the line is added exactly when `expected != contract.get("baseline_revision")`.
   - This text goes to the conductor through `RequestError` / `ValueError`, a machine channel (`human-questions.md:9-11`), so
     FR-6 does not govern it.

   Expected from FR-1 (what is wrong, what was expected), FR-2 (a door in the refused party's set, §2 facts) and FR-57 (a ban
   never a dead end: the "capture no baseline" move).
8. **A non-dict `baseline_contract` / `runtime_provenance` is refused by name (G-3, FR-1).** In `validate_baseline_request`,
   inside the `phase == "baseline"` branch:
   - `contract = request.get("baseline_contract")`. None or absent -> `{}`. Any other non-dict (truthy or falsy: `"x"`, `5`,
     `["x"]`, `""`, `[]`) -> append `f"baseline_contract must be a JSON object, got {type(value).__name__}: build it with
     `controller.py --operation baseline-inputs`"` and return the errors collected so far, together with the runtime line below
     if that applies. The key checks are skipped, because they cannot be read.
   - `runtime = request.get("runtime_provenance")`. None or absent -> `{}` (the revision line of item 7 then says `None`). Any
     other non-dict -> append `f"runtime_provenance must be a JSON object (the provenance probe's record), got
     {type(value).__name__}"` IN PLACE OF the revision line.
   - `{}` for either keeps today's behaviour: the "requires <key>" errors for the contract, and the revision line for the
     runtime.

   In `validate_managed_gate`, read `contract = request.get("baseline_contract")` once and use `contract if isinstance(contract,
   dict) else {}` at the three reads (:77, :86, :93). A non-dict contract then refuses with today's own sentences ("baseline
   case has no unique approved baseline contract" or "baseline Gate A reference is not the task's current approved decision").
   It never crashes and never passes.

   Test: one new parameterised method, for example `test_a_malformed_baseline_block_is_named_not_crashed`, with a `subTest` per
   row.
   - `validate_baseline_request`, `baseline_contract` = `"x"`, `["x"]`, `5`, `""` -> no exception; the errors hold "baseline_contract
     must be a JSON object, got <type>".
   - `baseline_contract` = None, and absent -> no exception; the errors hold "baseline_contract requires case_id".
   - `baseline_contract` = `{}` -> the same "requires" errors.
   - `runtime_provenance` = `"old"`, `["old"]`, `5`, `""` (with `contract()`) -> no exception; the errors hold "runtime_provenance
     must be a JSON object" and NO line starting with the revision sentence.
   - `runtime_provenance` = None, and absent -> the revision line of item 7, holding `None`.
   - `runtime_provenance` = `{}` -> the same revision line.
   - `build_baseline_fields(row, "gate-A", "old")` -> `ValueError` naming runtime_provenance, not `AttributeError`.
   - `validate_managed_gate` over the managed-state world of `test_managed_state_rejects_arbitrary_gate_reference` (:127-135),
     with `baseline_contract = "x"` -> a non-empty list and no exception.

   Expected from FR-1, the error direction (a refusal, never a pass) and AR-28.

architecture content:
- `AR-9 -- the revision refusal names its door (baseline-inputs, or no capture: it blocks nothing); a non-dict block is refused by name; refusal_registry --check run`
- `AR-12 -- code_friction not measured: dormant for roles (s6.md:130)`
- `AR-13 -- the receipt's status word is read only through gate_template.acceptable`
- `AR-16 -- the registry text through the family's one builder registry_why when present`
- `AR-19 -- axis 5 prose twins walked by grep`
- `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured and named`
- `AR-22 -- baseline_identity.readiness lands with its reader; the readerless provenance.baseline is removed (grepped: 0)`
- `AR-28 -- absent, unaccepted, malformed or unreadable-registry input: gap or named refusal, pinned`
- `AR-29 -- xref/shape checks, owner data, census units unchanged`

judgment content: `none -- a membership join of the producer's status word and two shape refusals; whether the capture proves the old build stays code's equalities`.

tests-over content: only if `tools/test_volume.py` asks: "C3-g: three parameterised tables in a keep file; the S-b refusal had no unknown-revision pin and no malformed-input pin".

Edges:
- E1 (absent / empty / other case / non-str status): not acceptable -> no count -> gap. INVARIANT: a receipt that does not say
  `captured` exactly never counts as before-evidence.
- E2 (unreadable registry; G5, G7):
  - Every receipt is uncounted, so every baseline row has a gap; `ready` stays True and nothing blocks.
  - The reason names the registry exactly where `matching` was non-empty, that is where at least one receipt met every equality
    of the filter (:189-198), whatever its word. The source-revision and hash checks (:201-214) are not part of that test. Every
    other row keeps "missing, stale or incomparable".
  - TEMPORAL, both worlds of C3-reg-precondition: before it lands on the base, item 3's reason is the only sign of a broken
    registry on this road. After it lands, `controller.validate` stops the next dispatch first, and item 3 is belt-and-braces
    inside a stage that began before. No pin assumes either order.
  - INVARIANT: a broken registry never counts a receipt, and never says evidence is missing when a matching receipt was there
    unjudged (FR-41).
- E3 (present but incomplete registry): the file parses but lacks the consumer. `registry_problem()` is "", so the reason stays
  the old sentence and nothing counts. This is the false-cause residue that C3-reg-precondition E2 accepts. CI holds it: A26
  `--check` and item 4's `captured` control row turn red on a consumer-id typo. INVARIANT: no false count.
- E4 POSITIONAL: the predicate filters `matching`, which is built from the equalities in their order; the source-revision and
  hash checks still follow. INVARIANT: a `captured` receipt for another case, version, gate or revision, or with changed
  evidence bytes, is never counted (the predicate is never the only guard, C3-0 E4).
- E5 TEMPORAL (receipts on disk): receipts written before C3-g carry the same two words from the same two producers. INVARIANT:
  no recorded receipt changes meaning (E-a).
- E6 TEMPORAL (consumer):
  - Before C3-g, `provenance.baseline` exists with no reader. After it, that consumer is gone and `baseline_identity.readiness`
    exists with its reader, in one commit.
  - C3-k3 is based after C3-g (F-k4 (b)) and adds `baseline_identity.capture` with its reader.
  - INVARIANT: no `accepts` entry without its reader (AR-22).
- E7 TEMPORAL (S-f): the pins are deltas from the base. C3-b2, C3-d and C3-reg-precondition may merge before or after C3-g. A
  later merger merges main in, re-derives its own row's pins and re-measures D13 (D-0048). INVARIANT: S-f (pins equal the live
  registry; no card edits another row's pin).
- E8 (limit): none introduced. `{expected!r}` is a value the request already carries; no truncation is added.
- E9 (shared block with C3-k3; G2, F-k4 (b)):
  - `gate-registry.json` and `test_gate_registry.py` are row-disjoint, except the F1 block and K-N2.12 NEG, which C3-k3 also
    edits after C3-g.
  - C3-g edits only the `baseline_identity` lines of F1 and the NEG case.
  - INVARIANT: after C3-k3, both `baseline_identity.readiness` (under `baseline_identity`, reader
    `baseline_contract.deployment_readiness`) and `baseline_identity.capture` (under `provenance_acceptance`, reader
    `manual_evidence.validate_baseline_record`) exist with their F1 pins. k3 adds its pin beside C3-g's and never replaces it.
    The two ids do not collide: `acceptable` resolves by the full consumer key (`gate_template.py:67-68` on main), and F-f
    checks per id (`gate_registry.py:724-727`).
  - The matching text for the k3 card is in «Edits owed to the j-k cards».
- E10 (adversarial inputs of the reused predicate, error direction): `acceptable` errs only toward False, so every doubt is a
  gap, never a count. The inputs that must stay on the safe side are item 4's word rows and a registry row with `field` null (a
  dict is refused). INVARIANT: `deployment_readiness` can count only fewer receipts than today, never more.
- E11 (the row's two reads; G6):
  - The row's unknown WORD, `inconclusive`, is never refused. It takes the declared safe default: an `awaiting_baseline` gap,
    never a count, with `next_action` offering baseline sources (FR-59's safe-default road; item 4's `inconclusive` row is its
    S-b pin).
  - The row's `refuse_with_door` describes the REQUEST site (`validate_baseline_request`). That site refuses an unknown or other
    old-build revision, and after item 7 its refusal carries the door.
  - `unknown_branch` has no runtime reader (grep over `scripts/*.py`: `gate_registry.py` only, t-1090 G6).
  - INVARIANT: C3-g changes neither `ready` nor `blocks_execution`, and the row's `refuse_with_door` holds with its door.
- E12 (one road, P31): the receipt's word is accepted at one site through the one predicate (verified one reader). INVARIANT: a
  second reader of `status` is a review finding.
- E13 (the door, positional): the door clause is appended AFTER the unchanged first clause, under the unchanged condition.
  INVARIANT: every request refused today is still refused (same condition), no request accepted today is refused (item 5's
  `old` row), and a reader of the first clause still matches.
- E14 (non-dict input, positional): the shape test runs BEFORE any `.get` on the value. INVARIANT: a malformed block is a named
  refusal, never an `AttributeError`, and never a pass. None, absent and `{}` keep today's errors exactly.

Measurement:
- The vacuous recorded-data control is replaced by item 4's table.
- The critic's control is `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --sites`, filtered
  for `baseline_contract.py` and `manual_evidence.py:728`. Before: no `baseline_contract.py` line. After: still none, plus one
  new line `manual_evidence.py:728 [baseline_identity]`.

---

## §3. Card C3-g2 — one reader of the baseline receipts; an unread receipt is "not known" (G1 analogs) — after C3-g and C3-reg-precondition

**Why a second card.**
- The two analogs live in `controller.py` (`Controller.deployment_inputs`) and `delivery_summary.py` (`_comparison_readiness`).
- `controller.py` is HOT, and C3-reg-precondition owns a block of it (`Controller.validate`, parent spec :1179-1180). It is
  built and in its fix round, so it is not merged.
- Putting `controller.py` into C3-g's owns would make two open nodes edit the HOT file. So the analogs are a separate card with
  its own owns, queued after C3-g (they share `baseline_contract.py` and `test_baseline_contract.py`) and after
  C3-reg-precondition merges.
- No j-k card names `controller.py` or `delivery_summary.py`. Grep count over the j-k spec gives 5, all `manual_evidence.py`;
  the same call counts that name, so the control is positive.

**Facts (read today).**
- `controller.deployment_inputs` (`controller.py:2252-2263`) calls `json.loads(path.read_text(...))` on every
  `work/baseline-receipts/*.json` with no guard (:2258-2259).
  - A file that is not JSON raises `JSONDecodeError`.
  - A JSON value that is not an object reaches `deployment_readiness` and crashes at `r.get` (:189).
  - Both stop `controller.py --operation deployment-inputs` (:10047-10048), which the conductor's phases call (`s5.md:379`,
    `s6.md:142`).
- `delivery_summary._comparison_readiness` (:148-179) skips a file it cannot read or that is not an object (:157-162). The row
  then reads "baseline evidence missing, stale or incomparable", which `render` shows a person (:569-574). That says "missing"
  for evidence that may be there unread (FR-41).
- These are two readers of one folder with two behaviours, which is one action on two roads (P31, AR-15).
- `hooklib.read_json(path, default, *, kind=...)` (`hooklib.py:873-890`) is the package's one JSON file reader (axis 16). With
  `kind=dict`, any unreadable, non-JSON or non-object file is `default`.

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/human-questions.md` (:1-63)
- this card, §2 (C3-g, merged before this card), and S-a..S-f of the parent spec (:278-346)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
  - `scripts/baseline_contract.py` (whole, as C3-g left it)
  - `scripts/hooklib.py:873-905`
  - `scripts/controller.py:2252-2263, 10045-10048`
  - `scripts/delivery_summary.py:148-179, 565-574`
  - `scripts/tests/test_baseline_contract.py` (whole)
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py` (new `load_receipts`; `deployment_readiness`: the `unread` keyword, the non-dict skip, the unread reason)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py` (`Controller.deployment_inputs` only) — HOT
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/delivery_summary.py` (`_comparison_readiness` only)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` (one new parameterised method, item 4)
non-goals:
- the registry, the predicate, `validate_*` (C3-g)
- `delivery_summary.render` and its default reason (:177), which stays
- any new key in the gap dict or in `deployment_readiness`'s result (FR-14)
- any controller raise (fork G-6 (b)), so `controller-blocks.md` does not move
- `judgment-census.json`; any new test file; quarantined files
handoff: report path given by the Lead
edges: E-g2.1-E-g2.7 below
DoD: `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, and D13 is unchanged (measured before and after). Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/baseline_contract.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/controller.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/delivery_summary.py C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py` and every printed non-slow file, at least `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_baseline_contract.py`. If `test_judgment_census.py` is printed and reports a C1 problem for `load_receipts`, stop with a question: no census row is expected. The slow printed files are named in the report for the canon.
siblings:
- axis 16 (`hooklib.read_json`): the new reader calls it.
- the third reader of the folder: `stand_identity.py:218` lists `baseline-receipts` as a protected folder, a path list and not a reader. Named, no edit.
- the two writers (`baseline_contract.write_baseline_receipt:159`, `manual_evidence.write_baseline_receipt:730`): unchanged.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` (C3-g2)

Items:
1. **`baseline_contract.load_receipts(task_root) -> tuple[list, list]`**, a new function next to `deployment_readiness`.
   - It reads `Path(task_root) / "work" / "baseline-receipts"` and visits `*.json` in `hooklib.sorted_paths` order. Each file is
     read with `hooklib.read_json(path, _UNREAD, kind=dict)`, where `_UNREAD = object()` is a module sentinel.
   - A dict is appended to `receipts`. Anything else appends the file NAME (`path.name`) to `unread`.
   - An absent folder returns `([], [])`. The function never raises: it reads a folder the factory writes, and its callers report.
   - The import of `hooklib` sits at the point of use (the file's style).
   - The name matches no census unit pattern, and the function raises nothing, so no census row is owed.
2. **`deployment_readiness(rows, receipts, task_root, expected_gate_ref=None, unread=())`.**
   - A member of `receipts` that is not a dict is never read. It is counted as one more unread entry (its name is
     `"<entry N>"`). This is the crash site of the controller analog.
   - For a row with no valid receipt, the reason is chosen in this order:
     - (1) C3-g's registry reason, when its condition holds;
     - (2) else, when the unread count (len(`unread`) + the non-dict members) is above zero: `f"{n} saved before-state
       capture(s) of this story could not be read, so whether this case has a valid one is not known"`;
     - (3) else "baseline evidence missing, stale or incomparable".
   - The gap dict and the result keep their keys.
   - FR-6: the new sentence is in words and names no file, no JSON and no path (`human-questions.md:57-59`). FR-41: an unknown
     is said as not known.
3. **The two callers take the one reader.**
   - `Controller.deployment_inputs` replaces its loop (:2256-2259) with `receipts, unread = load_receipts(self.store.root)` and
     passes `unread=unread`.
   - `delivery_summary._comparison_readiness` replaces :155-162 with `receipts, unread = load_receipts(task)` and passes
     `unread=unread`.
   - Neither caller parses a receipt any more (AR-13, AR-15).
4. **Test.** One new parameterised method in `test_baseline_contract.py`, for example
   `test_an_unread_receipt_is_not_known_never_missing`, with a `subTest` per row. Expected values come from FR-41, FR-1 and the
   one-road rule, never from the old output.
   - `load_receipts`, absent folder -> `([], [])`.
   - `load_receipts` over a folder holding one valid receipt (written by `B.write_baseline_receipt` as in :24-34), a file
     holding `not json`, a file holding `["captured"]`, and an empty file -> `receipts` is the one valid dict, `unread` has the
     three names in sorted order, and no exception is raised.
   - `deployment_readiness([row], [["captured"]], root)` -> no exception; the gap reason contains "could not be read" and "not
     known", and not "missing". This is the controller's crash class.
   - `deployment_readiness([row], [], root, unread=["a.json"])` -> the same reason.
   - `deployment_readiness([row], [<valid receipt>], root, unread=["a.json"])` -> `comparisons_ready` True and no gap. Unread
     files never hide a valid one.
   - `delivery_summary._comparison_readiness(task, [row], {})` over a task folder whose only receipt file holds `not json` ->
     the gap reason is the "not known" sentence (FR-41). Control: the same task with no receipt file -> "baseline evidence
     missing, stale or incomparable".
   - One-road pin: the source of `controller.Controller.deployment_inputs`, read with `ast`, calls `load_receipts` and holds no
     `json.loads`. No cheap behavioural world exists for that method, which needs controller state and Gate A. This row is the
     wiring check of the caller the behavioural rows cannot reach.

architecture content:
- `AR-13 -- the receipt files are read through hooklib.read_json at one reader`
- `AR-15 -- two readers of baseline-receipts become one survivor, load_receipts`
- `AR-28 -- an unreadable or non-object receipt: no crash, the gap says not known, pinned`
- `AR-29 -- no census unit added; owner data`

judgment content: `none -- reading a factory-written folder and naming what could not be read; no check of meaning`.

Edges:
- E-g2.1 (empty folder / absent folder): `([], [])` -> the old sentence. INVARIANT: nothing on disk is still "missing".
- E-g2.2 (an unread file beside a valid receipt): the valid one counts, and no gap. INVARIANT: an unread file never hides a
  valid capture, and never makes one count.
- E-g2.3 (the reason precedence, positional): registry, then unread, then missing. INVARIANT: each reason said is true. The
  word "missing" is said only when nothing could be unread or unjudged.
- E-g2.4 TEMPORAL: before C3-g2, the controller crashes and the summary says "missing". After it, both say "not known". The
  receipts on disk are not rewritten. INVARIANT: no reader of the folder remains outside `load_receipts`.
- E-g2.5 (limit): none. The sentence carries a count and no names, so there is no truncation.
- E-g2.6 (conflict, HOT `controller.py`): C3-g2 is dispatched only after C3-reg-precondition merges. INVARIANT: no two open
  nodes edit `controller.py` at once.
- E-g2.7 (an encoding or BOM file): `read_json` reads `utf-8-sig`, so a BOM is not unread (`hooklib.py:876`).

---

## §4. Card C3-h — stand_identity, converted by S-b/S-c alone (B-257) — wave 3, last on the S-f order

**Facts (read today).**

- **No accept site.** The row's five sites (registry :11-15) are:
  - `runtime_probe.conclude` and `finish` (produce);
  - `gate_preflight._derive_probe`, `named_container_said` and `driver_stage_build.build_outcome` (dispatch).

  The probe's `result` words are written by the producer (H4):
  - `runtime_probe.conclude` (`runtime_probe.py:1031-1056`: `unknown` final at :1043-1046, `sha_record("matched")` :1050-1052,
    `sha_record("mismatched")` :1053-1056);
  - `runtime_probe.finish` / `finish_unknown` (:1273-1294: `record["result"] = "unknown"` :1290; the evidence for
    matched/mismatched/person_confirmed :1282-1285).

  `_derive_probe` routes all five words into helpers (`gate_preflight.py:4587-4601`; an unknown sixth word goes to
  `_probe_defect`). So `vocabulary: code` is honest with the words unchanged.
- **H-1 (a) stands; the decisive evidence (H5).**
  - `named_container_said` returns '' exactly on `result == "matched"` (`gate_preflight.py:4484-4485`).
  - On '' the driver runs `probe_move` (`driver_machine.py:2644-2648`), which is `runtime_probe --suggest --write`
    (`driver_gates.py:630-636`). That writes one config entry, `execution.runtime_probes.<profile>`: a probe COMMAND, with no
    verdict and no evidence (`runtime_probe.py:1510-1519`). Its verification is "ALWAYS a rehearsal (S14)" that writes nothing
    (:1526-1527).
  - The driver says so: "No waiver is recorded (nothing is passed: the next rehearsal proves the stand with the registered
    probe's own check)" (`driver_machine.py:2637-2638`).
  - The rehearsal's own registration road registers on `unknown` as well as `matched` (`gate_preflight.py:4587-4592` ->
    `_probe_unknown` :4522-4525 -> `_probe_derived` :4317-4328, `argv` handed to the driver). So registering a probe is not an
    acceptance of the stand's identity anywhere.
  - Every later consumer runs the registered command and judges its fresh word: `build_outcome` at stage entry, and
    `execution_request.validate_request:175-179` at launch.
  - So the '' gates a config write that passes nothing. The E-c invariant "a re-role never hides a literal acceptance" is not
    engaged.
  - The two roads differ on `unknown` (rehearsal: matched and unknown; named container: matched only). That is a P31 question,
    returned as fork H-2.
- **The unknown branch, stated by fields (H1).** `driver_stage_build.build_outcome` (:401-418):
  - an `unknown` whose record carries `asks_person` in (`how`, `confirm`) raises the question (:402-412);
  - an `unknown` on a stand whose policy row is `person_confirms` is a status line (:413-417);
  - every other `unknown` is one printed line, "unread", and the stage GOES ON (:418).

  The method's docstring says "a doubt is a line, never a question and never a silent pass - the run path still refuses a build
  nobody could prove" (:300-301). The launch refuses an `unknown` (`execution_request.validate_request:175-179`).

  So the row's `question / wait / stage_entry` covers the ASKABLE unknown. The unaskable one takes the declared safe default
  (FR-59): a line at entry, and the launch refuses. The decided branch does not change.
- **S-b is already pinned.**
  - The probe level is pinned in the row's `test` file, `test_stand_identity.py`, which tests the row's producer.
  - The stage level is pinned in `test_story_run_stand_identity.py`, which is the `test` of the sibling row `stand_check`
    (registry :476). The row's own `test` stays, because the probe is the row's producer and the stage is `stand_check`'s.

  The card adds NO test row and NAMES the pins (item 2).
- **Measuring "S-b red today" (H2): a slot the Lead fills at dispatch.**
  - The Lead names a canon run in which the `package-full` job ran and the stand-identity test files passed (the run id, the
    job, and the two files' lines from `python -B tools/ci_read.py`).
  - Without it, the builder first runs `test_stand_identity.py` and `test_story_run_stand_identity.py` once and reports any red
    before editing. Those two named files are an exception to builder-rules :50-53 for this slot only, because the Lead's
    brief says so.
  - The old witness, run 44052586866, does not witness them: `package-fast` was skipped and there was no `package-full`
    (t-1090 rerun).

given:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/design/factory-rules.md` (whole)
- `C:/QAFactory/forge-repo/plans/builder-rules.md`
- `C:/QAFactory/forge-repo/docs/TESTING.md`
- this card, and S-a..S-f of `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-phase2-cards-spec.md` (:278-346)
- read, under `C:/QAFactory/forge-repo/ai-packages/qa-factory/`:
  - `references/gate-registry.json:7-36`
  - `scripts/gate_registry.py:485-681` (the `vocabulary` rule :512-519)
  - `scripts/driver_stage_build.py:295-422`
  - `scripts/tests/test_stand_identity.py:813-965`
  - `scripts/tests/test_story_run_stand_identity.py:444-498, 550-598, 997-1023`
  - `scripts/tests/test_execution_request.py:693-764`
  - `scripts/tests/test_gate_registry.py`: the debt/converted pins, K-T1.2, the split, K-T1.14, the F4 list and its flip control, D13
- E4 SLOT (the Lead fills it at dispatch): «canon run <id>, job package-full, `test_stand_identity.py` <line>, `test_story_run_stand_identity.py` <line>» — or «none: run the two files first»
owns:
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json` (row `stand_identity` only: `vocabulary`, `status`, `debt_ref`)
- `C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` (the S-f pins of `stand_identity` only)
non-goals:
- any code (`runtime_probe.py`, `gate_preflight.py`, `driver_stage_build.py`, `driver_machine.py`, `stand_identity.py`)
- the row's words, `verdict_map`, sites and roles (H-1 (a)), `accepts`, branch, `policy_file`, `scope_keys`
- `test_stand_identity.py`, `test_story_run_stand_identity.py` and `test_execution_request.py` (pins named, not edited); `judgment-census.json`; any new test file
- the two registration roads (fork H-2)
handoff: report path given by the Lead
edges: E1-E8 below
DoD: The E4 slot is honoured first (the Lead's run, or the builder's one run of the two files, reported before any edit; a red is a stop). Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/gate_registry.py --check` exits 0, and `stand_identity` is absent from the `N gate(s) left as debt:` block. Then `python -B C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/scenario_walk.py --witness-for C:/QAFactory/forge-repo/ai-packages/qa-factory/references/gate-registry.json C:/QAFactory/forge-repo/ai-packages/qa-factory/scripts/tests/test_gate_registry.py` and the printed non-slow files. The batch canon judges `test_gate_registry.py`, `test_stand_identity.py` and `test_story_run_stand_identity.py`; the report names them, with item 2's pins.
siblings:
- axis 5 (`docs/SIBLING_MAP.md:143`): the words do not change, so no prose twin is walked.
- the five sites keep their roles (H-1 (a), evidence above).
- the two carriers of the person's word, `state/stand-confirmations.jsonl` and `records/stand-identity.json`: named, unchanged.
- the two probe-registration roads that differ on `unknown`: fork H-2.
designer: `C:/QAFactory/forge-repo/docs/tasks/specs/20261117-rules-debt-wave3-g-h-cards-r2.md` (C3-h)

Items:
1. **Registry row `stand_identity`.** Set `vocabulary: "code"`, `status: "converted"`, `debt_ref: ""`. Every other key is
   unchanged.

   Expected from S-c (the words are the probe's own `result` words, written by `conclude` / `finish`) and `_check_row` :516-519
   (a converted row must say `code`).
2. **S-b: named, no row (H1, H3).** The report quotes each pin with file:line on the base tree. The builder re-greps each by its
   label.
   1. `test_stand_identity.py:818-820` — a read device build that cannot be identified: `unknown`, `asks_person: "how"`.
   2. `test_stand_identity.py:833-837` — the person's word on the same build: `person_confirmed`, bound to the image.
   3. `test_stand_identity.py:840-843` — a rebuild voids the word and asks again.
   4. `test_stand_identity.py:887-896` — an unreadable build: `unknown`, NO question, no word taken, an error that says why.
   5. `test_stand_identity.py:932-939` — another story's word is not taken (also from a copy in the other story's file).
   6. `test_stand_identity.py:941-944` — a moved stand definition voids the word.
   7. `test_stand_identity.py:957-960` — a recorded `command` row reads the commit: `matched`.
   8. `test_story_run_stand_identity.py:449-450` — K36 setup: the askable unknown asks at stage entry and waits (exit 3, kind
      `stand_identity`, variant `how`).
   9. `test_story_run_stand_identity.py:481-498` — "always confirm" writes a `person_confirms` row and the stage goes on.
   10. `test_story_run_stand_identity.py:583-597` — a recorded `command` method makes the next probe read this story's commit.
   11. `test_story_run_stand_identity.py:1008-1023` — K39: an unknown with nobody to ask (and four probe failures, an unknown
       word, a matched that proves nothing) is ONE printed line, no question (exit 0), and the role starts.
   12. `test_execution_request.py:764` — «K-N2.2 control: an `unknown` is refused, whatever it names»: the launch refuses an
       unknown record (`validate_request`).

   Pins 1-7 live in the row's own `test` file. Pins 8-11 live in `stand_check`'s test file: the stage half of the branch. Pin 12
   is the launch.

   If a pin is gone on the base tree, the node stops with a question (the Lead opens the fix node). No row is invented here.
3. **S-f pins** (deltas from the base, measured at the build):
   - `EXPECTED_DEBT` loses `stand_identity` and `EXPECTED_CONVERTED` gains it, with an AR-20 comment naming C3-h and its task.
   - K-T1.2 becomes N-1.
   - The split: +1 / -1, and the K-T1.14 label words.
   - The F4 `code` list gains `stand_identity`.
   - D13: re-measure with `GR.analyse` before and after. Expected: no triple and no item moves. `analyse` does not read
     `vocabulary` (`gate_registry.py:843-878` uses anchors and `_row_words`), and neither the words nor the sites change. A
     different measurement is a stop and a question.

   The F4 flip control copies `registry["rows"][0]` (that is `stand_identity`) and overrides `vocabulary`, `status`, `test`,
   `sites` and `accepts`, so it survives this conversion unchanged.

architecture content:
- `AR-28 -- the askable unknown asks at stage entry and waits (K36); the unaskable one is a line and the launch refuses it (K39, test_execution_request K-N2.2); the probe level pinned in test_stand_identity ep1_41e`
- `AR-29 -- no check moves; registry row only`
- `AR-20 -- debt -1, converted +1, F4 +1, D13 re-measured: no move`

judgment content: `none -- a registry row converted with no code; the person's word stays the person's, read through the existing stand-identity carriers`.

tests-over content: not expected (no test lines added).

Edges:
- E1 (the unknown branch, split per H1):
  - (i) An ASKABLE unknown (`asks_person` how/confirm) -> the question at stage entry, and the stage waits (pin 8; pins 1, 3).
  - (ii) An unknown with NOBODY to ask (an unreadable build, docker down, a probe failure, an unknown word) -> one printed line,
    and the role starts (pins 4, 11). The run is then refused at launch by the provenance predicate (pin 12).
  - (iii) An unknown on a `person_confirms` stand -> a status line (`driver_stage_build.py:413-417`).
  - INVARIANT: no run on an unproven build, because the launch refuses it (AR-28, FR-59). "S5 never starts" is NOT the
    invariant.
- E2 (the person's word, scope): a word binds to its story and its build (image). A policy-file row binds to its `scope_keys`
  (`environment_id`, `profile_id`). INVARIANT: a word given for another story, another build or a moved stand definition never
  covers this one (pins 3, 5, 6).
- E3 TEMPORAL (S-f, order): C3-h is last on the expected order (parent spec :330-331). Its pins are deltas from whatever merged
  before it. INVARIANT: S-f.
- E4 TEMPORAL (red today; H2): the slot of §4 facts. With the Lead's canon run, the builder edits. Without it, the builder runs
  the two files once first. A red pin is a stop: the red line goes to a fix node that owns the failing site, and C3-h follows
  it. INVARIANT: a row is never converted over a red unknown-branch pin.
- E5 (limit): none introduced.
- E6 (conflict, HOT `gate_preflight.py`): C3-h edits no `gate_preflight.py` code, so its queue position binds only if a red S-b
  (E4) or fork H-2 adds a code site. INVARIANT: no two open nodes edit the HOT file at once.
- E7 (the flip control, positional): the F4 control reads `rows[0]` and overrides every key it relies on. INVARIANT: the control
  never depends on a live row's status (C3-0 E10).
- E8 (one road, P31): no new reader of the probe's words; the five sites stay the only ones registered. The registration roads'
  difference on `unknown` is fork H-2.

---

## §5. Forks (returned, not decided)

- **G-5 — which family form the registry-unreadable gap reason takes** (C3-g item 3). The brief says "use the family's one
  builder function if present on the base, else the C3-reg-precondition prefix". On the C3-b2 worktree the family has two
  forms of one fact (`gate_template.py:60-68`):
  - the in-line form, "the gate registry cannot be read (R): a factory defect, <tail>", used by every site that judges a reuse
    (`execution_request` `_match`, `proof_level` run and receipt);
  - the stop form, "gate registry unreadable: ...", whose prefix `tools/controller-blocks-gen.py` matches as the dispatch stop.

  Options:
  - (a) The in-line form: `registry_why(problem, tail)` when present, else the same bytes written in place. A gap reason is a
    site judging a receipt, not a dispatch stop.
  - (b) The stop prefix "gate registry unreadable:", as the brief's literal words say. A non-stop line would then carry the
    stop's prefix, which a generator matches.
  - (c) (a), with the tail and the reason in person words, because this line reaches a person (FR-6): "the factory could not
    judge the saved before-state capture (a defect of the factory's install, not of the story)". This leaves the family text.

  **Rec (a)**: one builder, one fact (AR-16, P31), and the same shape as its three sibling sites. The "(R)" text is
  `load_registry`'s short sentence, which a person already sees at the family's other person-facing sites. Cost of (c): a
  second sentence for one fact. The card executes on (a).
- **G-6 — a non-object receipt at `controller.deployment_inputs`: report or refuse** (C3-g2). The brief cites FR-1 ("a refusal
  names what it expected") for the controller analog.
  - (a) The controller refuses with a named `StateConflict` ("work/baseline-receipts/<f> is not one JSON object ... move it
    aside, then run deployment-inputs again"). The summary reports "not known". That is two roads for one fact. The refusal
    joins `controller-blocks.md` (regenerated), and `deployment-inputs` stops.
  - (b) One road: both callers take `load_receipts`, and the unread receipt becomes a "not known" gap reason that names what
    was expected (a readable capture).

  **Rec (b)**:
  - `deployment_readiness` never blocks (docstring :176-182), and `s5.md:370-377` says baseline never blocks execution.
  - P31 forbids the two roads. Designer rule 6 puts the one-road option first.
  - The FR-1 content (what was expected) is in the reason.
  - Cost of (a): one controller raise with its door, a `controller-blocks.md` regeneration, a controller-world test, and a
    second behaviour for one fact.
  - The card executes on (b).
- **G-8 — the same two classes in C3-k3's function `manual_evidence.validate_baseline_record`.** Found by the sweep, not
  carded here.
  - Class 1: a truthy non-dict `baseline_contract` passes :670 (`or {}`) and crashes at :674 (`contract.get`). A non-dict
    `runtime_before` / `runtime_after` crashes at :680/:688/:690.
  - Class 2: the sibling sentence "manual baseline runtime must match baseline revision" (:689) names no door.
  - That function is owned by C3-k3 (j-k spec :623). Editing it here would make two open cards edit one function.

  Options:
  - (a) Add to the k3 card the item text in «Edits owed to the j-k cards» below, item E-k3-g8, fixed in k3's round.
  - (b) Widen C3-g's owns to `validate_baseline_record`'s guards and serialise k3 behind it. This collides with k3's rewrite of
    the same function.

  **Rec (a)**. It is not a finding, per the owner's word; it is an item of the card that owns the function. Cost: one item and
  one table row in k3.
- **H-2 — two probe-registration roads differ on `unknown`** (P31; critic t-1090 noticed analog).
  - The rehearsal registers a derived probe on `matched` AND `unknown` (`gate_preflight.py:4587-4592`, `_probe_unknown` ->
    `_probe_derived`).
  - The named-container road registers only on `matched` (`gate_preflight.py:4484-4485`, `driver_machine.py:2633-2648`).
  - Neither passes anything (H5 evidence).

  Options:
  - (a) One road, aligning the named-container road with the rehearsal: an `unknown` answer also registers the named
    container's probe, since registration is a config write the next rehearsal re-proves. This is a node C3-h2 owning
    `gate_preflight.named_container_said` (HOT) and the probe loop of `driver_machine.py:2639-2650`, with one test row (an
    `unknown` named-container answer registers and records nothing passed).
  - (b) One road the other way: the rehearsal registers only on `matched`, and an `unknown` becomes a card.
  - (c) The difference is legal (a named container that cannot be verified is likely the wrong name). This needs the owner's
    word, quoted with its carrier.

  **Rec (a)** as the one-road option (designer rule 6). The choice between (a) and (b) is a product question for the owner
  (which answer a person gets after naming a container). Cost of (a): one node on a HOT file, queued after C3-h. Until it is
  decided, C3-h is executable unchanged.

## §6. Small choices closed

- C3-g imports `gate_template` at the point of use (the file's lazy style).
- The registry reason applies exactly where `matching` is non-empty (G5). A row with no matching receipt keeps "missing", which
  is true.
- `inconclusive`'s unknown owner is `environment`, as the row's `unknown` owner is today.
- G-3's falsy non-dicts (`""`, `[]`, `0`) are shape errors too. Only None and absent read as an empty block, so a value the
  request carries is never silently dropped.
- The door text uses `{!r}` of the two revisions: a machine channel, a value the request carries, no truncation.
- C3-g2's unread sentence carries a count and no file names (FR-6 forbids naming a factory JSON record in a person's line). No
  key is added to carry the names (FR-14).
- C3-g2's wiring row for `deployment_inputs` is an `ast` read, because that method has no cheap behavioural world.
- Every test goes into the keep file `test_baseline_contract.py` (the quarantined `test_handoff_producers.py` and
  `test_human_reading.py` are avoided).
- C3-h adds no test row, because twelve pins exist (item 2, enumerated).

## §7. Readers of every touched file (rule 7)

Commands (Grep, today):

| # | path | pattern | result | positive control |
|---|---|---|---|---|
| 1 | `tools/` (count) | `baseline_contract\|test_baseline_contract\|deployment_readiness\|load_receipts\|validate_baseline_request\|delivery_summary\|deployment_inputs\|provenance\.baseline\|registry_why` | 1 hit: `tools/fixtures/dispatch_manifest/K8.txt:11` (a prose fixture naming `delivery_summary` among t-053's files) | the hit itself |
| 2 | `tools/` (count) | `gate-registry\|test_gate_registry` | 16 hits in 3 files: `source-split-carriers.json` 3, `source_split.py` 12, `test_quarantine.py` 1 | the hits |
| 3 | `tools/` (count) | `controller\.py` | 12 hits in 5 files: `controller-blocks-gen.py` 4, `test_forge_metrics.py` 5, `test_dispatch_gate.py` 1, `test_controller_blocks_gen.py` 1, `test_collect_intake.py` 1 | the hits |
| 4 | `.githooks/` | the names of 1-3 + `architecture_gate` | 1 hit, `commit-msg:37`, which is the control, so 0 for the names | `architecture_gate` |
| 5 | `.claude/settings.json` | the names + `hygiene_gate` | 1 hit, `:38`, which is the control, so 0 for the names | `hygiene_gate` |
| 6 | `.claude/agents/` | the names + `designer` | 3 hits, all `designer.md`, which is the control, so 0 for the names | `designer` |

| touched | reader | verdict |
|---|---|---|
| `gate-registry.json` (C3-g row `baseline_identity`, C3-h row `stand_identity`) | `tools/source-split-carriers.json`, `tools/source_split.py`, `tools/test_quarantine.py` (path only); package: `gate_registry.py` (A26), `gate_template.py`, `test_gate_registry.py` | unchanged: the row form is kept. The pins change in each card (S-f), and then in C3-k3 (owed edits below) |
| `test_gate_registry.py` (C3-g, C3-h) | `tools/source-split-carriers.json` (D13 carrier), `tools/source_split.py` (selftest strings), the `test-layers.json` keep row | unchanged: the triple tuple form is kept. Shared pins change in every converting stream (S-f order, D-0048); the F1/NEG block changes in C3-k3 by the owed text |
| `baseline_contract.py` (C3-g, C3-g2) | tools: 0. Package: `execution_request.py:124-127`, `manual_evidence.py:660-673`, `controller.py:2240-2262`, `delivery_summary.py:154-169`, `run_suite.py:2393-2394`, `test_baseline_contract.py`, `test_live_audit_contract.py:45-53`, `test_story_root_class.py:863` | the callers of `validate_*` are unchanged: same signature, more text after the same prefix, a named error instead of a crash. The `deployment_readiness` signature gains a defaulted keyword (C3-g2), so old callers are unchanged. `controller.py` and `delivery_summary.py` change in C3-g2 |
| `test_baseline_contract.py` | `test-layers.json:213` keep row; tools: 0 | unchanged |
| `controller.py` (C3-g2, `deployment_inputs` only) | `tools/controller-blocks-gen.py:22` (reads its raises), `tools/test_controller_blocks_gen.py`, `tools/test_forge_metrics.py`, `tools/test_dispatch_gate.py`, `tools/test_collect_intake.py` (path strings) | unchanged: C3-g2 adds no raise (G-6 (b)), so `controller-blocks.md` does not move. Under G-6 (a) it would be regenerated in C3-g2 |
| `delivery_summary.py` (C3-g2) | `tools/fixtures/dispatch_manifest/K8.txt` (prose); package: `factory_dashboard.py:1148` (reads `comparison_gaps`), the quarantined `test_handoff_producers.py:207-226` and `test_human_reading.py:231-234` | unchanged: the gap keys are kept. The quarantined tests read `reason` as whatever it is (`:222` concatenates it), so they hold |

## §8. Remarks -> where applied

| remark | where applied |
|---|---|
| G1 owns for findings; the two analogs | Void by the owner's word (no finding). G-2 is fixed in C3-g item 7, G-3 in item 8. The analogs are card C3-g2 (§3), with its own owns, because `controller.py` is HOT under C3-reg-precondition |
| G2 F-k4 collision; E9 invariant | §2 facts (F-k4 = (b)); item 1; E6; E9 (the invariant verbatim in substance); «Edits owed to the j-k cards» (E-k3.5, k3 owns, item 2, item 7) |
| G3 accepting control; the row shape | item 5: row `old` (no error, no raise); the approved-row shape of :118-121 named |
| G4 section B; family prefix | §1 FR walk (B: FR-3, FR-6); item 3 (human-questions statement; the family builder); fork G-5 |
| G5 one conjunct list; E2 wording; broken registry + inconclusive | item 2 (`matching` / `candidates`); item 3 condition on `matching`; item 4 rows (inconclusive and another-version under a broken registry); E2 |
| G6 E11 two reads | E11 rewritten; item 4 `inconclusive` row named as the S-b pin; the door now lands (item 7), so `refuse_with_door` holds with its door |
| G7 E2 temporal | E2, both worlds of C3-reg-precondition |
| H1 E1 wrong | §4 facts (the branch by fields, `driver_stage_build.py:401-418`); E1 split (i)-(iii); pins 4, 8, 11, 12 |
| H2 E4 witness | §4 facts slot; `given:` E4 SLOT line; DoD first sentence; E4 |
| H3 pin count | item 2: a numbered list of twelve, no count word in the text |
| H4 the producer, not the seed | §4 facts: `runtime_probe.conclude` :1031-1056, `finish`/`finish_unknown` :1273-1294 |
| H5 the H-1 trail | §4 facts «H-1 (a) stands; the decisive evidence»; the P31 analog is fork H-2 |

## §9. Edits owed to the j-k cards (the Lead applies them to `docs/tasks/specs/20261117-rules-debt-wave3-j-k-cards.md`; this designer does not write that file)

F-k4 = (b) (Lead, 17.11.2026). Replacement texts:

1. **k3 `owns:` line** (j-k :627). Replace «row `baseline_identity`: `provenance.baseline` removed if still there (F-k4)» with:
   > row `baseline_identity`: no edit (F-k4 (b): C3-g removed `provenance.baseline` and owns `baseline_identity.readiness`)
2. **k3 `given:`** (j-k :621). Replace «the merged C3-g diff if any» with:
   > the merged C3-g diff (required: k3 is based after C3-g)
3. **k3 item 2, registry sub-bullet** (j-k :647-648). Replace it with:
   > Registry: `"baseline_identity.capture": ["matched", "not_applicable"]` under `provenance_acceptance` (F-k4 (b)). Its prefix
   > names `baseline_identity` (`promotable: false`), so a `person_confirmed` added later is a finding. `baseline_identity`'s own
   > `accepts` (`baseline_identity.readiness`, C3-g) is not touched.
4. **k3 item 7, the F1 and NEG bullets** (j-k :675-679). Replace «F1 :639-641: the two ids are replaced by ...», «The F1 loop
   :648-656 runs on the new ids ...» and «K-N2.12 NEG :291-298 uses `baseline_identity.capture`» with:
   > - F1: the check of `provenance.environment_preparation` becomes `home["environment_preparation.deploy_proof"] ==
   >   "provenance_acceptance"`. A NEW check `home["baseline_identity.capture"] == "provenance_acceptance"` is ADDED. C3-g's check
   >   `home["baseline_identity.readiness"] == "baseline_identity"` stays as C3-g wrote it. The check of the consumers under
   >   `provenance_acceptance` gains the two new ids (the list and its label's count word re-derived from the live registry).
   > - F1 «both guarding rows are promotable false» stays.
   > - The F1 loop runs on three pairs: C3-g's `("baseline_identity.readiness", "baseline_identity")`, unedited;
   >   `("baseline_identity.capture", "baseline_identity")`; and `("environment_preparation.deploy_proof",
   >   "environment_preparation")`. Each gives exactly one finding, naming the consumer and the guarding row.
   > - K-N2.12 NEG: a SECOND case is added. `person_confirmed` is appended to `baseline_identity.capture` and gives exactly one
   >   finding naming the consumer and the word. C3-g's case on `baseline_identity.readiness` stays unedited.
5. **E-k3.5** (j-k :694-696). Replace it whole with:
   > - E-k3.5 TEMPORAL (C3-g, F-k4 (b), Lead 17.11.2026): k3 is based after C3-g. C3-g removed `provenance.baseline` and added
   >   `baseline_identity.readiness` (under `baseline_identity`, reader `baseline_contract.deployment_readiness`) with its F1 and
   >   K-N2.12 NEG pins. k3 adds `baseline_identity.capture` (under `provenance_acceptance`, reader
   >   `manual_evidence.validate_baseline_record`) with its own pins. If the base still holds `provenance.baseline` (C3-g not
   >   merged), k3 stops with a question and removes nothing. INVARIANT: after C3-k3, both `baseline_identity.readiness` and
   >   `baseline_identity.capture` exist with their F1 pins; k3 adds its pin beside C3-g's and never replaces it; no consumer
   >   exists without a reader; and every guard pin (F1, K-N2.12 NEG) counts exactly one finding per consumer.
6. **Fork F-k4 text and the Lead line** (j-k :436-451, :883-886): the Lead records F-k4 = (b) there. This draft does not word it.
7. **E-k3-g8, a new k3 item on fork G-8 (a)** (insert after k3 item 2):
   > 2b. **`validate_baseline_record`, malformed blocks and the doorless sibling** (owner's word 17.11.2026: fixed in the round).
   > (i) `contract = record.get("baseline_contract")`: a non-dict other than None/absent appends "baseline_contract must be a JSON
   > object, got <type>" and is read as `{}` for the remaining checks. `runtime_before` / `runtime_after`: a non-dict other than
   > None/absent appends "runtime_before (or runtime_after) must be a JSON object (the provenance probe's record), got <type>"
   > and is read as `{}`. No `AttributeError` reaches the caller.
   > (ii) :689 «manual baseline runtime must match baseline revision» keeps its words as the prefix and appends ": the probe's
   > expected_source_revision is {x!r}, the approved baseline_revision is {y!r}. Capture again on a stand that runs that
   > revision, or record no baseline: missing before evidence blocks no current check".
   > Test rows (in the keep file `--witness-for` prints for `manual_evidence.py`): `baseline_contract` = `"x"` -> the named
   > error, no exception; `runtime_before` = `"x"` -> the named error, no exception; None -> today's "baseline missing ..."
   > errors; a mismatching `expected_source_revision` -> the error holds the door substrings; the matching control -> no such
   > error. INVARIANT: a malformed manual baseline is a named refusal, never a crash and never a pass.

## §10. Not established

- No run: `gate_registry.py --check` / `--sites`, `GR.analyse`, `refusal_registry.py --check`, and the test files. The D13 delta
  of C3-g is the critic's run (t-1090). Those of C3-h and C3-g2 ("no move") are by reading the scanner rules; the builder
  measures them.
- Whether `refusal_registry.py`'s wide scan keys any entry on the exact text of `baseline_contract.py:23`. SCANNED (:63-64)
  holds only guard files, and the list transport never creates a unit (`test_judgment_census.py:235-237`). The prefix is kept
  anyway (item 7), and the DoD runs `--check`.
- Whether the base for C3-g holds `registry_why` (it is on the C3-b2 worktree, in its RD1-27 round). Item 3 covers both worlds.
- Whether `human_text` checks a `comparison_gaps` reason. No such reader was found in `delivery_summary.render` (:569-574); the
  rest of the module was not searched.
- The canon state of the two stand-identity files (the E4 slot).

## §11. Reading trail

- Given: the t-1085 cards (whole); the t-1090 verdict (whole); the j-k cards :420-479, :619-708, :870-893 (+ grep
  `k3|E-k3.5|baseline_identity|provenance\.baseline`).
- main, under `ai-packages/qa-factory/`:
  - `scripts/baseline_contract.py` (whole);
  - `scripts/manual_evidence.py:655-739`;
  - `scripts/controller.py:2215-2274, 10025-10064`;
  - `scripts/delivery_summary.py:140-184, 560-579`;
  - `scripts/execution_request.py:110-184`;
  - `scripts/refusal_registry.py:55-99, 1827-1866` (+ def grep);
  - `scripts/tests/test_judgment_census.py:77-92, 150-259`;
  - `scripts/hooklib.py:873-898`;
  - `scripts/runtime_probe.py:1031-1058, 1270-1294, 1505-1529` (+ grep);
  - `scripts/driver_stage_build.py:295-422`;
  - `scripts/driver_machine.py:2626-2649`;
  - `scripts/driver_gates.py:628-639`;
  - `scripts/gate_preflight.py:4315-4330, 4476-4487, 4510-4525, 4580-4602`;
  - `scripts/tests/test_baseline_contract.py` (whole);
  - `scripts/tests/test_stand_identity.py:812-961`;
  - `scripts/tests/test_story_run_stand_identity.py:444-453, 995-1029`;
  - `scripts/tests/test_execution_request.py:740-764, 1325-1349` (+ grep `unknown`, `def verdict`);
  - `scripts/tests/test_handoff_producers.py:185-229`;
  - `scripts/tests/test_human_reading.py:215-244`;
  - `references/human-questions.md:1-64`;
  - `references/environment-preparation.md:40-118`;
  - `references/role-commands.json:1-30`;
  - `skills/qa-story/phases/s5.md:362-391`, `s6.md:124-153`;
  - `design/architecture.md:105-164` (+ change-check grep).
- The C3-b2 worktree: `scripts/gate_template.py` (whole); `scripts/tests/test_gate_registry.py:288-305, 640-679, 1175-1218`
  (+ grep of the pins); the grep for `registry_why|gate registry unreadable|gate registry cannot be read` over `scripts/`
  (control for main's 0); the grep of `baseline_contract.py` defs.
- Greps with controls:
  - `baseline runtime must match|approved before revision` (the hit at `baseline_contract.py:23` is the control);
  - `deployment_readiness|baseline-receipts|...` over the package;
  - `deployment_inputs|baseline_inputs|_comparison_readiness`;
  - `baseline-inputs|evidence_phase|expected_source_revision` over `*.md`;
  - `comparison_gaps|awaiting_baseline`;
  - `validate_managed_gate`;
  - `test-layers.json` for the four test files;
  - the j-k spec for `controller.py|delivery_summary.py` (count, control `manual_evidence.py`);
  - `role-commands.json` for `baseline` (control: its own entries, read);
  - the rule-7 greps of §7.

## Lead decisions on the forks of round 2 (17.11.2026)

- G-5 = (a): the in-line family form `registry_why(problem, tail)`.
- G-6 = (b): one road — both callers take `load_receipts`; an unread receipt is a "not known" gap reason naming what was expected.
- G-8 = (a): fixed inside C3-k3's round (item E-k3-g8 of §9), told to the k-cards designer t-1101.
- H-2: the choice (a)/(b) is the owner's (what a person gets after naming a container); asked 17.11. C3-h is dispatched unchanged meanwhile.
- E4 SLOT of C3-h: canon run 44059237092 (branch `worktree-agent-ac40b44fb0a175afa`, full canon, `python -B tools/ci_read.py why 44059237092` -> "success: nothing failed"; the package-full-report job ran).
- No second plan-critic pass: round 2 applies the verdict t-1090 and adds no architecture change; the Lead checked §8 (every remark placed) and §5.
