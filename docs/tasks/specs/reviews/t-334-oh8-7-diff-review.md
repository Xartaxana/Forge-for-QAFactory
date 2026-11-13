# t-334 — critic diff gate: OH8-7 (t-329), staged in worktree oh8-7 (wip/oh8-7, base 6e3133f)

Verdict: **fit_with_fixes**. 0 blocking findings. 3 fixes, all to text: two to the commit message, one to the C7/BLIND_SPOT wording. The acceptance decision and the `tier:` line belong to the full Lead (rule 6).

## Empirics first (rule 13): my own reruns on the staged tree, in place, nothing committed or unstaged
- `test_judgment_census.py`: **26/26 ok**, exit 0. Totals: `951 units ... conductor=491 ... subclass_family=55 subclass_pending=190 (ceiling 190)`. Every problem class is empty.
- `test_refusal_registry.py`: **336/336 ok**, exit 0. `refusal_registry.py --check`: `A24 refusal registry: no violations`, exit 0.
- Default path: `sites()` over SCANNED gives **80** (first `codex_roles.py::export`, last `stage_guard.py::check_command`). Over `scan_files` it gives **953**. Both equal the builder's "before".
- Per-file vs global (B3), stdin probe: global matching gives 1666 widened sites, per-file gives 1498. Per-file adds 0 sites of its own. **All 168 dropped sites are true non-family raises**: `Refusal` from changelog_assemble, grounding_table (incl. `GT.Refusal` in base_slice/blast_radius/reference_snapshot), manifest_from_tests and driver_core (`Refusal(Exception)`; `ReworkRefused(Refusal)` in driver_dispatch); `Refused` from collect_pack (`Refused(Exception)`, :68). So the scoping drops nothing it should keep.
- Spec-named mutation (§B.5 "no closure"), run in-process by monkeypatching `raise_family` to literals only, no file touched. Red rows: direct, grandchild, attr_base, nested_class, multiple, cross_module, alias, attr_subclass, neutral_only. Restored: green. This complements the builder's mutation (global matching), which reds shadowed_local, C3 and C7.
- Scanned stems that collide with stdlib names: none. Assignment aliases of family names (`E = A`): 0. Added package lines with Cyrillic: 0.

## Key 1 — t-326 B1-B4 in the code
- **B1 (c1): holds.** u3 units are still created only from the default `sites_by_file` (test_judgment_census.py:244-245). Blocks come from `wide` (:249-262). A widened site that hits no unit goes into `pending` and never creates a unit. The `neutral_only` row asserts no C1 line and `pending_names == ["helpers_x.py::f"]`. The default return shape of `sites()` is unchanged (FR-14).
- **B2: holds.** `SUBCLASS_PENDING_CEILING = 190`. `_c7` is red above (`> ceiling`) and below (`lower the constant to n`). `test_neg_pending_is_dense_and_only_shrinks_c7` drives both directions plus equality. It is not a `ratchet` key, so `REQUIRED_CEILING_KEYS` and gate item 7 are untouched. The axis-18 row is in SIBLING_MAP.
- **B3: holds**, by the probe above and the rows shadowed_local, shadowed_import, no_binding (`ImportError(ValueError)` in mod_a does not capture an unbound builtin raise) and alias (counted). Rule 15 is satisfied: a name counts in F only through F's own binding (raise_family's import loop: `local not in fx["classes"]`, plus the per-file `fam[f]`).
- **B4: holds.** In `_raised_here`, an `ast.Attribute` callee returns False when `raises is None`. The row `attr_raise` flips only with a spec, and the attr/default test asserts `sites(files=...) == []` for that source.

## Key 2 — A24 unchanged; the E4 deviation
I traced the default path. With `raises=None`, `_raised_here` reduces to `isinstance(func, ast.Name) and func.id in REFUSAL_RAISES`, which is the old predicate byte for byte, read at call time. No caller of A24 passes `raises`. The numbers reproduce (80/953). **The deviation is acceptable.** The structural test proves (i) every default call's callee is a literal `Name`, (ii) the default set is a subset of the widened set, and (iii) the default and `raises=None` agree. That is stronger than comparing lengths plus first and last keys, and it does not go stale when OH8-6 adds sites. Only (iii) is tautological, since both calls take the same default. It is harmless.

## Key 3 — FR-59 / AR-28: routes where an unknown passes
- **F1 (fix, text): the count ceiling cannot see a swap.** If one pending function is closed and a new subclass-only refuser is added in the same diff, the count stays 190 and C7 is green. `_c7`'s docstring ("a new one is red") and its message overstate this. The axis-18 duty (critic q9) does not catch it either, because a swap is not a raise. Fix: say "a count: a swap of one pending function for another is not seen" in the `_c7` docstring and in BLIND_SPOT/about/docstring. Optional: pin `pending_names`. This is not blocking: it is the property of the bound I proposed in t-326 B2, and the road is temporary.
- Misses that are named and true: stdlib subclass, tests-only class, `make()` base, `raise A`, `raise A()` (the `no_arg` row proves it). Unnamed and minor, with no instance measured in the package: (a) `raise cls(...)` through a variable or assignment alias (0 assignment aliases measured); (b) a class base `mod.B` where `mod` comes from `from pkg import mod`. `_file_bindings` maps only `import` aliases into `mods`, so `classes` resolves `a`-refs only through `import X`. Fold both into F1's wording. The wording "a base that is not a plain name" is slightly loose, because `alias.Name` bases ARE resolved. Suggested: "a base that is not a name or `module.Name` of an imported scanned module".
- An unparsable file is left out of the family and falls back to the literals (`raises.get(name, literals)`). The census's C1 unparsable rule still reports it. No pass on an unknown.

## Key 4 — standing questions
- **DUPLICATION/CONSISTENCY (q6):** none found. I grepped the package for `replace(".", "/") + ".py"` and for `def _?(module_file|resolve_module|module_path|class_family|subclass|imports_of|file_bindings)`. The nearest relatives are `manifest_from_tests._module_files`, which resolves PROJECT test imports (another domain), and `_imports_of` in scenario_walk and test_driver_layers (test helpers). None is a survivor for package class-family resolution. AR-13 is kept: the census holds no `ast.Raise` (grep: 0 hits in the census, positive control refusal_registry.py:1086).
- **CODE QUALITY (q7):** acceptable. `raise_family` is a bounded fixpoint (the cycle row passes). An attribute callee whose `.attr` is a literal (`self.ValueError(...)`) is accepted for any receiver: over-inclusion, the safe side of E1. `units_of` now parses each file twice more (`raise_family` plus the widened `sites`), and that cost is not stated truthfully (F2). The parameterised row test stops at the first red, but each assert names its case id (P16).
- **q9, ratchet raise named:** `blocking_per_role.conductor` 476 -> 491. The reason is "census widened to subclass raises (OH8-7)", over 15 rows, all conductor, with no `blocks_override`. The count matches t-326's measured 20 minus the 5 cross-file collisions, and my census run (conductor=491, C3 empty). No other key moved: breach 1, `MEANING_CEILING` 24, overrides 10. New member SUBCLASS_PENDING_CEILING = 190, measured dense.
- **q10, four questions:** present for the new constant. (c) names test_c7 and calibration check 35 (b). (d) names CI.
- **q11, judgment:** the line is the literal E9 form, and `architecture_gate.py` exits 0 on the message. No class is judged and no meaning row is added. The 15 flips are existing rows.
- **q12, one road (P31):** the temporary second road is bounded by the counted constant. Its follow-up carrier (fix 11 of the t-326 BINDING section) is the coordinator's move at acceptance. It is still owed. Without it, the BLIND_SPOT pointer "OH8-7b and after" has no target.

## Key 5 — the commit message
- `mechanism_gate.py` fails only on the missing `tier:` line. That line is expected from the full Lead.
- **F2 (fix):** four-question item (a) says "parses each file once more". It is twice (`raise_family` plus `sites(raises=)`). Correct the text.
- **F3 (fix):** DoD 10 requires `architecture: AR-29, AR-20, AR-13, AR-22, AR-28`. **AR-22 is missing.** The gate passes without it, but the spec demands it. Add a line along the lines of `architecture: AR-22 -- the new totals fields family/pending/pending_names are produced by units_of/analyse and read by totals_line, _c7 and the tests`.
- The axis block enumerates all 36 axes (36 `## Axis` headings in the map). The covered lines for 18, 32 and 34 are true by the diff. The n/a lines are plausible, and I spot-checked 16 (no JSON reader touched) and 17 (no verdict shape touched).

## Class completeness (rule 5 / rule 14)
Surface: the refusal-raise name resolver of `refusal_registry`. Neighbouring classes walked:
- naming: collisions (probe), shadowing (rows), stdlib-name file collisions (0);
- nesting: transitive classes, nested classes, cycles;
- encoding: the attribute form;
- empty or broken input: no-arg raises, unparsable files.

Map: axis 18 (new row, covered), axis 32 (the one scanner, kept), axis 34 (temporary road, bounded).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1: _c7 docstring/message and BLIND_SPOT/about/docstring say the pending bound is a COUNT (a swap of one pending function for a new one is unseen); also name raise-through-variable/assignment alias and a mod.B base via from-import of a module; tighten 'a base that is not a plain name' (alias.Name bases are resolved)",
    "F2: commit message four-question (a): the census parses each file twice more (raise_family plus sites(raises=)), not once",
    "F3: commit message adds the DoD-10 line architecture: AR-22 -- new totals fields family/pending/pending_names have producer and readers"
  ],
  "class_completeness": "Surface: the refusal-raise name resolver. Per-file scoping probed on the real package: 168 sites dropped vs global matching, all true non-family (Refusal/Refused of Exception, driver_core, GT), 0 added. Neighbours: shadowing, alias, no-binding, cycle, nested, attr form, no-arg, unparsable, stdlib-name collisions (0). Axis 18 new member row present; axis 32 kept (no ast.Raise in census); axis 34 bounded by SUBCLASS_PENDING_CEILING, follow-up carrier owed by the coordinator (t-326 binding fix 11). Residual: count ratchet blind to swaps (F1).",
  "trail": {
    "read": [
      "staged diff git -C .claude/worktrees/oh8-7 diff --cached (5 files, 284+/29-)",
      "worktree test_judgment_census.py:238-269, :302-318, :602-623",
      "spec t-321 part B 285-363, Lead decisions 367-384, Critic t-326 fixes 386-420",
      "reviews/t-326-oh8-7-plan-review.md",
      "reports/t-329-oh8-7-commit-msg.txt",
      "grep class Refusal|Refused|ReworkRefused in scripts; grep ast.Raise; grep module/class resolvers for duplication; grep C-key readers in tools and scripts"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_judgment_census.py (worktree package root)", "result": "26/26 ok, exit 0; conductor=491, subclass_family=55, subclass_pending=190 (ceiling 190)"},
      {"command": "python -B scripts/tests/test_refusal_registry.py; python -B scripts/refusal_registry.py --check", "result": "336/336 ok exit 0; A24 no violations, exit 0"},
      {"command": "python -B - stdin probe: default sites, per-file vs global family", "result": "sites() 80 (codex_roles.py::export .. stage_guard.py::check_command), scan_files 953; global 1666 vs per-file 1498 sites, 0 per-file-only, 168 dropped all Exception-based Refusal/Refused"},
      {"command": "python -B - stdin: in-process no-closure mutation of raise_family on SUBCLASS_ROWS", "result": "red direct, grandchild, attr_base, nested_class, multiple, cross_module, alias, attr_subclass, neutral_only; restored green"},
      {"command": "python -B tools/architecture_gate.py and tools/mechanism_gate.py on the proposed message", "result": "architecture exit 0; mechanism exit 1 only for the missing tier: line (Lead-owned)"}
    ]
  }
}
```
