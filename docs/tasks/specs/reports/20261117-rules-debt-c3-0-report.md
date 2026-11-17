# C3-0 report (t-1038) - the one predicate for true accept sites

## What changed
- `ai-packages/qa-factory/scripts/gate_template.py` (new): `acceptable(value, consumer, *, registry=None)` and `registry_problem(*, registry=None)`. One reader: `gate_registry.load_registry` / `structural_error` (reused, AR-13), read once per process into `_READ`. No CLI, never raises (a broad `except` returns False / a reason). Class space per item 2: matched -> token `matched`; person_confirmed -> token AND row `promotable is True`; not_applicable -> bare token or `not_applicable:<reason_code>`; unknown/mismatched/other -> False. All row-word comparisons sit in `acceptable` only (the registered site).
- `references/gate-registry.json`: one site line `{"file": "gate_template.py", "function": "acceptable", "role": "library"}` at the end of row `provenance_acceptance` sites. No `accepts` entry added.
- `scripts/tests/test_gate_registry.py`: `predicate_cases()` (one table, 39 rows) + `part_predicate()` (runs it, plus registry-unreadable by an empty plugin root, and `registry_problem` rows), wired in `main()`; F4 flip control moved onto an in-memory copy row `flip_probe` (plus a `code` control); D13 triple and count.
- `scripts/tests/test-layers.json`: `"gate_template.py"` in `covers` of keep row `test_gate_registry.py`.

## Pins old -> new (re-derived on this head, S-f)
- debt block 8 -> 8, converted 19 -> 19, K-T1.2 "8" unchanged (no row converts; `--check` prints "8 gate(s) left as debt" before and after).
- `D13_ITEM_COUNT` 140 -> 146 (measured with `gate_registry.py --sites --json`: 140 before, 146 after). Six comparisons attributed to the new site: `cls == 'matched'`, `'matched' in tokens`, `cls == 'person_confirmed'`, `'person_confirmed' in tokens`, `cls == 'not_applicable'`, `'not_applicable' in tokens` (the last two count because `not_applicable` is a word of the row `provenance_acceptance`, which registers the site). The card expected the count from the anchor comparisons; it did not name the two `not_applicable` ones.
- `D13_TRIPLES` + `("gate_template.py", "acceptable", "provenance_acceptance")`.
- Line moves: the card's registry lines (:65-68) now hold `gate_registry.py` sites at 65-68 as stated; `test_gate_registry.py` F4 control was at :753-756 (still there), D13 block now ~:913+ .

## Witness
`python -B ai-packages/qa-factory/scripts/gate_registry.py --check` -> `A26 gate registry: no violations`, `8 gate(s) left as debt:`, rc=0.

`scenario_walk.py --witness-for <the four owns>` printed: `scripts/gate_template.py: keep test_gate_registry.py (layer gate_named, covers it)`; test_gate_registry.py -> the six scenario files + test_scenario_walk.py; test-layers.json -> test_selftest_shard.py, test_selftest_slow_tests.py. Non-slow files run (python -B each):
```
test_scenario_cart_1: scenario cart-1: 15/15 ok
test_scenario_dry_1: scenario dry-1: 9/9 ok
test_scenario_local_1_0108: 15/15 ok
test_scenario_local_1_arm_b: 5/5 ok
test_scenario_walk: 95/95 ok
test_scenario_world: 33/33 ok
test_selftest_shard: 95/95 ok
test_selftest_slow_tests: 124/124 ok   (all rc=0)
```
`test_gate_registry.py` and `test_judgment_census.py`: slow, not run whole - judged by the batch canon.

## Scratch run of the new rows (source: C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\501cb4e0-b55f-46d8-9262-11b1caefad61\scratchpad\scratch_c30.py)
It imports `test_gate_registry`, calls `predicate_cases()`, compares each row with `gate_template.acceptable`, then calls `part_predicate()`, then runs a NAIVE predicate (any exact word of the row accepted, class and promotable ignored) over the same rows as the negative control. Output:
```
(rows: 39 cases; every "PASS C3-0 acceptable <case>" line, "PASS C3-0 registry-unreadable ...", five "PASS C3-0 registry-problem ..." lines; no FAIL)
NEGATIVE CONTROL: naive predicate fails 7 rows: ['record-unknown', 'never-unknown', 'never-mismatched', 'person-not-promotable', 'na-reason-unlisted', 'row-without-verdict_map', 'class-outside-the-five']
```
(The first line of the scratch output, "rows: N failing with the real predicate: []", was cut off by `tail`; the PASS lines show no failure. Row count per `predicate_cases()`.) Also called directly: `part_site_attribution()` and `part_fix_pass()` - all D13 and F4 lines PASS, including the new `flip_probe` control.

## FR walk
- A (refusals): no refusal site added; no text shown to a person. n/a otherwise. FR-4: no informed pass is checked. FR-5: n/a.
- B: text to a person unchanged (module docstring is for developers; registry_problem returns the loader's reason text).
- C: FR-13 closed variety stays data (no word list in the module; tokens/words come from the row); FR-12 no phrase list; FR-14 output shape: bool / str, documented; FR-39 n/a.
- D: FR-58 expected values from FR-59 and the registry grammar, never the predicate's output; FR-59 every unknown -> False; FR-41 n/a; FR-16 n/a.
- E, F: not touched.
- G: FR-30 English only, no Cyrillic; FR-29 no escape sequences; FR-45 writes nothing; FR-47 instrument, not a role's judgment; FR-54 siblings below.

## Architecture / commit
AR-13 one reader (load_registry reused); AR-15 one predicate for a true accept site; AR-28 unknown never accepts (table); AR-29 xref, owner data, no census unit; AR-20 D13 +6 re-measured.

## Beyond the manifest / analogs
- Read beyond given: `scripts/tests/harness.py` (check helpers), `tools/test_volume.py` (not run usefully, no output).
- Analog named, not swept: `profile_contract.acceptable_provenance` (F-T2: raises ValueError on an unknown token, this predicate does not, by design).
- Spec divergence: item 8 spoke of the "anchor comparisons"; the scan also attributes the two `not_applicable` comparisons (6 total, not 4).
- OPEN QUESTION (found, not fixed - audit_factory.py is not in owns): `audit_factory.a1_findings(plugin root)` now returns `gate_template.py is reachable from nothing - not in hooks.json, not imported by a referenced hook, not in CLI_SCRIPTS: dead code shipped as if it ran` (measured: `python -B -c` calling `A.a1_findings`, filtered on gate_template). Until C3-b2 / C3-rr import it, this script has no importer. Door options for the Lead: add `gate_template` to `audit_factory.CLI_SCRIPTS` (as `gate_registry` is) in this node, or accept the finding until the first consumer lands. Whether a doctor test/pin of A1 goes red on it is for the batch canon (not run here).
- Commit: 9b0baa26 on worktree-agent-aa11322709a274e56 (amended once to add this line; see git log for the final sha). Pre-commit WARN (not a refusal): gate_template.py matches no feature in plans/features.json (doors b/d), not in owns, left to the Lead. docs/OWNER_PRINCIPLES_INDEX.md was regenerated by factory_rules_index.py as instructed and left unstaged.
