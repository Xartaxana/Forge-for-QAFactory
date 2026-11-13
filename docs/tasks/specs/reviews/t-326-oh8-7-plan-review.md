# t-326 — critic on plan: t-321 part B (OH8-7) + Lead decisions (F-B1 (d)/(c1), F-B2 (a), F-B3 (a), F-B4 (a))

Verdict: **NEEDS WORK (fit_with_fixes)**. 4 blocking findings (B1-B4), 4 minor (M1-M4). Every fix is an edit to the spec; no fork goes back to the owner.
Base: read-main = origin/main 6448fcc. Between 2f1cec8 (the Lead's measurement) and 6448fcc no file in this review's scope changed (`git diff --stat` on the 4 files: empty).

## Empirics first (rule 13): I re-ran the §B.2 measurement on read-main myself, plus the F-B3 variant and a collision probe
```
family beyond literals: 56
true collisions: [('Refusal','changelog_assemble.py'),('Refusal','driver_core.py'),('Refusal','grounding_table.py'),
                  ('Refusal','manifest_from_tests.py'),('Refusal','runtime_probe.py'),('Refused','collect_pack.py')]
bare raise: 0 | no-arg call (dropped by _key_text): 1 | attr-form family raises: 16
before      units 951  norow 0   breach 1 sites 953  conductor 476 (other roles = HEAD ceilings)
family      units 1223 norow 272 breach 1 sites 1649 conductor 496; C3: only `blocking_per_role.conductor` 496 > 476
family+attr units 1234 norow 283 breach 1 sites 1665 conductor 496; C3: same single line
```
Then I listed the 20 rows that flip: all have `roles: ['conductor']`, none has `blocks_override`. **5 of the 20 flip only because of a cross-file name match.** They are `changelog_assemble.py::check_arguments`, `::refuse_existing_version`, `::refuse_unseen_files`, `grounding_table.py::_refuse_call` and `manifest_from_tests.py::check_scope`. Each one raises a LOCAL `class Refusal(Exception)` (grep: `changelog_assemble.py:59`, `grounding_table.py:68`, `manifest_from_tests.py:184`). The name `Refusal` gets into the family only because `probe_by_code.py:204` defines `Refusal(ValueError)`.

## Key 1 — facts by trail
- `_refusal_calls` change point (`refusal_registry.py:1065-1074`): holds. It matches only `ast.Name` against the module global `REFUSAL_RAISES` (:59), which it reads at call time, so the measurement's monkeypatch is valid. Every other caller of `sites()` uses the default: `refusal_registry.py:1149, :1218`, `test_refusal_registry.py:41, :204, :228`, `test_doctor_context.py:582, :598` (grep `\bsites\(`, with the census call at :212 as the positive control).
- The C1 "no row" rule: holds (`test_judgment_census.py:290-294`). `_c3` counts only rows (:343-354), so the "existing rows only" reading of the measurement is right.
- Gate item 7 (v): holds (`architecture_gate.py` docstring and :268-284). A raise of only `blocking_per_role.*`/`safety` needs `adds data check` or `moves..to code`. Any other raised key, including a key the gate does not know, needs `moves..to code`.
- **The Lead's pasted line `name collisions: []` is false.** The spec's own script prints every family name with `len(defined) > 1`. `Refusal` is defined in 7 scanned files and `Refused` in 3 (grep `class (Refusal|Refused)`), so that script cannot have printed `[]`. The other numbers reproduce exactly. → M1.

## Key 2 — (d)+(c1): sound in direction, but the spec text implements (a), and the second road has no bound
**B1. Part B's body is written for (a), not for the chosen (c1).** Today `units_of` creates a u3 unit from every site (`add(file, s["function"], "u3")`, :234-235). So `sites(raises=family)` wired as §B.3.2 says gives exactly the measured 1223 units and 272 C1 reds. That is (a), not (c1). Edits to the spec:
- §B.3.2: `units_of` takes unit creation (u3) from `sites(files=...)` without `raises`, exactly as today. It takes `blocks` (the loop at :259-264) from `sites(files=..., raises=family)`. A widened site in a function that is not a unit by u1/u2/literal-u3/stages/A24 creates NO unit; it goes into the pending set (B2). State the cost of the second `sites()` parse, or have the one call return both lists. Either way the default return shape stays unchanged (FR-14).
- §B.5: the test expectation for every positive row becomes "flips `blocks` on a unit found by another route". Let the synthetic function be `check_f` (u1) and assert its `blocks`. Add one row `neutral_only`: `def f(): raise A('no')` with `class A(ValueError)` → no unit, and `f` listed as pending.
- §B.5 mutation: "C1 on the real census (new rows become stale)" cannot happen under (c1). The red becomes C3 `blocking_per_role.conductor is 476, below its ceiling 496`, plus the pending-count line (B2).
- §B.3.2 and §B.6.4: "subclasses are counted" and "old gap clause absent" are false under (c1). The clause is REWRITTEN, not removed: it says that a subclass raise flips `blocks` on an existing unit, and that a function refusing only through a subclass is pending, counted, and closed by OH8-7b and the nodes after it. `blind_spot_names_subclass_gap` then asserts the new clause.
- §B.0 handoff ("list of new rows") and E2 ("counted"): reword them for (c1).

**B2. The temporary second road is named but not bounded: a pass on an unknown (FR-59, AR-28).** After the node, 272 functions are pending (283 with F-B3 (a), measured). They refuse through a subclass, have no unit, and the census is green on them. A new subclass-only refuser added before OH8-7b lands is invisible: BLIND_SPOT prose catches nothing. "The end state equals (a)" also has no measure. Edit: the census computes the pending set, prints its size on the totals line, and holds it under a shrink-only, dense test constant, for example `SUBCLASS_PENDING_CEILING = <measured>`. It is red above the ceiling (a new pending refuser) and red below it (lower the constant). It is a test constant like `MEANING_CEILING` (:88), NOT a `ratchet` key. So `REQUIRED_CEILING_KEYS` and gate item 7 are untouched, and F-B4 stays (a). Each follow-up node lowers it; 0 is the (a) end state. This is a new axis-18 member: add a SIBLING_MAP axis-18 row in the same commit (rule 9), and give it a four-question block (DoD 10 already requires one). The value depends on B3.

**Is 476->496 the only raise?** Measured on (c1) with F-B3 (a) and global name matching: yes. It is the single C3 line, attribute raises add 0 flips, and `breach` stays 1. Under B3's scoping, the 5 collision flips leave: estimate 476->491, to be measured by the builder.

**B3. Global name matching is a false cross-match (rule 15) and makes E3 contradict E9.** The pair is "a raise names N" in file F plus "N has a family base" in file G. The two conditions are not scoped to the same binding, and that is the cause of the 5 false flips above. The same goes for `driver_*`: they raise `driver_core.Refusal(Exception)`, which puts 25+ false entries in the pending set (`driver_dispatch.py` alone). E3's remedy, `blocks_override: false` + `note`, raises `ratchet.blocks_overrides`. Gate (v) answers that raise only with `moves..to code`, and E9 then stops the node. So the spec's own remedy is unusable. Edit: in §B.3.1, `raise_family` returns the family per file. A raised name counts in F only if F's own binding of it is in the family: a local `ClassDef`, or `from M import N [as A]` where M is a scanned module whose `N` is in the family. A local non-family definition shadows a family class of the same name defined elsewhere. A name with no binding in F resolves only to the literals; for example, a package `class ImportError(ValueError)` (`import_test_receipt.py:26`) does not capture a builtin `ImportError` raised in another file. This also closes the `as B` alias miss, so the `alias` row of §B.5 becomes "counted". Add §B.5 rows `shadowed_local` and `shadowed_import` (each must stay unflipped), and drop E3's override remedy.

## Key 3 — §B.4 edges for the (c1) cut
- Name collisions: wrong as written (B3).
- Transitive subclasses: covered (E2 `grandchild`, E6 cycle). Fine.
- Attribute-form raises (F-B3 (a)): **B4.** §B.3.1 and F-B3 put the attribute acceptance "in the same `_refusal_calls` change" without gating it. If it is unconditional, the A24 default path widens too: +16 sites over the scanned files (measured over `scan_files`; over `SCANNED` not measured). That breaks the non-goal and E4. Edit: attribute acceptance only when `raises` is given. The attribute-form literal raises (`raise ES.StateConflict`) are then flip-only/pending under (c1), like subclasses. Say so.
- A subclass defined in `tests/`: E2 and `tests_only` are covered and named as a miss. Fine.
- Missing (M2): E1 says the scanner "never hides a raise of a family name it can resolve". That is false: `_key_text` (:1051-1053) drops a call with no args. I measured 1 family site of the form `raise A()`. Name it in BLIND_SPOT or fix E1's wording.
- E4's proof (equal lengths plus first and last keys) is weak. Also assert that every default site's raised callee is a literal `ast.Name` in `REFUSAL_RAISES`.

## Key 4 — F-B2 (a) and OH8-6
- A24 stays unchanged under a `raises=None` default, given B4's gate. All default callers are listed in Key 1. The A24 path never passes `raises`. Fine.
- One caution: if the builder writes `_refusal_calls(tree, raises=REFUSAL_RAISES)`, the default binds at definition time. That is harmless for A24 but breaks DoD 1. **M3.** DoD 1, "builder re-runs the §B.2 script on the node tree", is meaningless after the change: the census already passes the family, so the script's before/after both show the widened state. Replace it with: the builder pastes the node's totals line (with the pending count and family size), the intermediate C3 (476 ceiling) and the green run.
- OH8-6 overlap: **M4.** The disjointness is one-sided: spec t-324 does not exist yet (no file `t-324*` or `*oh8-6*` in `docs/tasks/specs`, root or read-main). Batch-8 l.37 lets OH8-6 touch "the places of the scout". It may add REGISTRY entries, which create A24 census units, need rows in `judgment-census.json`, and move the ceilings, or it may touch `SCANNED`. Edit §B.7: the t-324 dispatch's D-0048 list must exclude `_refusal_calls`, `sites`, `raise_family` and `REFUSAL_RAISES`. If OH8-6 adds a REGISTRY entry or edits the census JSON, a line `очередь: OH8-6 → OH8-7` (or the reverse) is written, and the later node re-measures the dense ceilings after merging `main`.

## Key 5 — feasibility and other changes
Feasible once B1-B4 are applied. It is about one builder node, and the census run is about 140 s. Also:
- E9: write the literal line, `judgment: adds data check refusal_registry.raise_family -- census sees refusals through package subclasses`. The `<unit>` slot must not stay a placeholder.
- The follow-up nodes OH8-7b and after need a carrier now (D-0044): rows in an untaken batch, each naming its file group and the pending-ceiling drop it delivers. Then the BLIND_SPOT pointer has a target.
- §B.1 AR-28 row: rewrite it to "the remaining misses are named AND the pending set is counted (B2)".

## Standing questions
- DUPLICATION/CONSISTENCY: none found beyond B3. Grepped for other AST class-hierarchy helpers: the spec's grep (`subclass|famil`) reports none, and I did not repeat it. The second road is B2.
- CODE QUALITY: plan only; C-B4 (the helper name must not match `UNIT_NAME_RE`) is right. `raise_family` matches no `UNIT_NAME_RE` alternative. Fine.
- ONE ROAD (P31, item 12): (c1) is a temporary second road, and the owner's word is not needed because (d) ends at one road. It is acceptable only with B2's counted bound and the follow-up carrier. Without them it blocks.

The acceptance decision belongs to the Lead tier (rule 6); this verdict is an input to it.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1: spec body (B.3.2, B.5, mutation, BLIND_SPOT rewrite, handoff) implements (a): units_of l.234-235 makes a u3 unit per site, so sites(raises=family) yields 1223 units / 272 C1 reds, not (c1)",
    "B2: the temporary second road has no counted bound: 272 (283 with attr form) subclass-only refusers are green with no ceiling; new ones are invisible (FR-59, AR-28)",
    "B3: global class-name matching is a false cross-match (rule 15): 5 of the 20 conductor flips raise a local Refusal(Exception); the E3 remedy (blocks_override) raises blocks_overrides, which E9 forbids",
    "B4: F-B3 (a) attribute acceptance is not gated on raises=, so A24 widens (non-goal, E4)"
  ],
  "fixes": [
    "B.3.2: u3 creation from sites() without raises; blocks from sites(raises=family); widened site in a non-unit goes to the pending set, never creates a unit",
    "B.5: positive rows assert blocks flip on a u1 unit check_f; add neutral_only (no unit, pending); mutation red = C3 conductor below ceiling 496 plus the pending line",
    "Rewrite BLIND_SPOT, about, docstring and the blind-spot check to the (c1) clause naming the pending set and OH8-7b; fix the B.0 handoff and E2 wording",
    "Add SUBCLASS_PENDING_CEILING, a shrink-only dense test constant (not a ratchet key), printed in totals; SIBLING_MAP axis-18 row in the same commit",
    "raise_family resolves per file (local ClassDef or from-import of a family class; local non-family definition shadows); add shadowed_local and shadowed_import rows; alias becomes counted; drop the E3 override remedy; re-measure the raise (estimate 476->491)",
    "Gate attribute-form acceptance on raises being given; state that attribute literal raises are flip-only under (c1)",
    "Correct the Lead section's false collision line (collisions: Refusal x5, Refused x1)",
    "DoD 1: replace the re-run of the B.2 script with the node totals line, the intermediate C3 and the green run",
    "E1: name the no-arg raise miss (_key_text drops it); strengthen E4 to literal-callee-only on the default path",
    "B.7: the t-324 D-0048 list excludes _refusal_calls, sites, raise_family, REFUSAL_RAISES; a queue line if OH8-6 touches REGISTRY or the census JSON",
    "E9: the literal judgment line naming refusal_registry.raise_family; follow-up nodes written into an untaken batch with their pending drops"
  ],
  "class_completeness": "Axis 32: the widening stays in the one scanner (F-B2 a), kept. Axis 18: the new pending ceiling needs a map row (fix). Axis 34: (c1) is a temporary second road, acceptable only with the counted bound and the follow-up carrier (B2). Surface = the refusal-raise name resolver; neighbouring classes walked: magnitude (272/283 measured), nesting (transitive, nested class: covered), naming (collisions B3, builtins, alias), empty/broken (no-arg raise M2, cycle E6).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-321-oh8-1-oh8-7-specs.md:155-471",
      "read-main ai-packages/qa-factory/scripts/refusal_registry.py:1040-1110, :56-59",
      "read-main ai-packages/qa-factory/scripts/tests/test_judgment_census.py:1-460",
      "read-main tools/architecture_gate.py docstring item 7 and :260-310",
      "read-main docs/SIBLING_MAP.md axes 18, 32, 34 headings and :562, :592",
      "read-main plans/piles/onboarding-hooks/batch-8 l.10-19, :37-38",
      "grep: class Refusal|Refused; raise Refusal|Refused per file; raise ImportError; sites( callers; REFUSAL_RAISES and _refusal_calls users"
    ],
    "reruns": [
      {"command": "python -B - <read-main plugin root> (the B.2 script plus an attribute-form variant and a collision probe, stdin heredoc, pure read)", "result": "family 56; units 951 -> 1223 (1234 with attr); norow 272 (283); conductor 476 -> 496 is the only C3 line; breach 1 unchanged; collisions Refusal x5, Refused x1; no-arg family raise 1; attr family raises 16"},
      {"command": "python -B - (list the rows that flip from non-blocking to blocking under the family)", "result": "20 rows, all roles [conductor]; 5 raise a local Refusal(Exception): changelog_assemble x3, grounding_table._refuse_call, manifest_from_tests.check_scope"}
    ]
  }
}
```
