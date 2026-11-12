# t-060 attempt 2 - TD-11 B0b fix round (critic verdict t-062)

Files changed (WT = C:\QAFactory\forge-repo\.claude\worktrees\td11-integration): `ai-packages/qa-factory/scripts/tests/test_driver_layers.py`; `ai-packages/qa-factory/scripts/tests/fixtures/driver-layers.json` (one header key added: `l8_skip`). Nothing else touched.

## Per finding

| id | how | fixture (each also runs under the `gizmo` header) |
|---|---|---|
| B1 | one rule for both cuts: in the L6/L12 loop a part imports a family module only if strictly lower-ranked or `<prefix>base`; equal rank (cycle included) is an L12 problem; the clause says nothing extra (it always runs once L10 holds) | "L12 (mixins cut) a part imports a part of the same rank"; "...two-way import cycle..."; "...strictly LOWER-ranked part" (none); "an equal-rank import of `<prefix>base` is legal" (none); the old "stays a matter of L6 alone" fixture is turned into the first |
| B2 | `PINNED_EXCEPTIONS` = the 8 map rows; new `pin_problems(rows, pinned, name, stale)`: analyse asks the new-row direction (L5), `real_maps` asks both (a fixture map is not the pinned family's map) | "pin: a map equal to its pin is clean / a ninth row is new / a pinned row the map no longer holds is a problem / analyse's own question is the new-row direction only / empty pin and no exceptions is fine"; real: "the pin equals the exceptions list, both directions" |
| F1 | `_install_calls` follows `import module_facade as x`, `from module_facade import install [as y]` (and `*`), `getattr(<module or alias>, "install")(...)`; `installed: false` refuses ANY import of module_facade in the facade (via `_imports_of`); (b) also needs the call as a module-body statement and `__name__` as first argument | "L11 (c) installed false with the install call made through <3 forms>"; "(b) installed true, through <3 forms>, is seen" (wrong order reported) and "in order" (none); "installed false with only an import"; "first argument is a literal, not __name__"; "install call is not at module level" |
| F2 | the L6/L12 loop uses `_imports_of` | "L12 an equal-rank import through importlib.import_module"; "L6 an upward import through __import__" |
| F3 | `L8_SKIP_BY_FACADE` deleted; header key `l8_skip` (list of file names, absent = empty) in the map, shape-checked in L10 | "L8 a file named in the map's l8_skip is not counted"; L10 "an l8_skip that is not a list", "an l8_skip entry with a path", "a well formed l8_skip" |
| F4 | `_parse_script` (utf-8-sig); L11 (a) reports an unparsable script by name | "L11 (a) a script that cannot be parsed is reported by name"; "a script that starts with a BOM is still read" |
| F5 | L10: duplicate stem in `layers`; `facade` must be `isidentifier()` (no crash: the file check runs only for identifiers); class tables (`attributes`, `state_keys`, `dynamic_state_keys`, `string_dispatch`) on `class: null`; map file name must be `<prefix minus _>-layers.json` (analyse/header_problems take `file_name`, `real_maps` passes it); `facade_clash_problems` (two maps, one facade) checked in `real_maps` | L10 header cases "a facade that is a path", "a module listed twice in layers", "a class table on a family whose class is null"; "a map file whose name does not match the prefix" (+ "wrong file name skips every other check of that map", + `@ok` none); "two maps naming one facade are a problem" / "distinct facades are no clash" |
| F6 | `facade_importer_problems(root, facades)` in `real_maps` (module_facade.py excepted, `scripts/tests/` not in the glob, unparsable scripts reported, import forms via `_imports_of`); green today | "E8 a script importing module_facade with no map is reported ..." and "every importer being a map's facade leaves only the unparsable script"; real: "every script that imports module_facade is the facade of a map (0 problem(s))" |
| F7 | `l12_class_use(..., in_part)`: the assembled class by name inside a part is refused; new `class_uses_outside_functions` scans module-level code and class bodies (decorators/defaults included) | "L12 the assembled class by name inside a part"; "...in the module-level code of a part"; "a wrong mixin at module level of the facade"; "...in a class body"; none: "the assembled class at module level of the FACADE is legal" |
| F8 | `per_file` and the unused `case` parameter of `problems_of` removed (call sites updated) | - |

## DoD witness (verbatim)

Command: `python -B C:\QAFactory\forge-repo\.claude\worktrees\td11-integration\ai-packages\qa-factory\scripts\tests\test_driver_layers.py`

```
driver-layers.json: census 1023 names defined by driver_chains.py, driver_timing.py, story_run.py (878 class members); map rows 1023; ... edges 5469 of which upward 8 (exceptions rows 8); source-text sites 66
driver-layers.json: not run / informational: L11 (b): not run for story_run: family.installed is false (the facade is not installed yet)
=== test_driver_layers: 283/283 ok ===
```
283 PASS, 0 FAIL (195 before). Hygiene on both files: non-ASCII 0, CRLF 0.

## Mutation probes (script `scratchpad/probe.py`, copies in a temp dir outside the repo, removed afterwards)

```
(a) L6: []
(a) L12: ['driver_stage_a.py:1 imports driver_stage_b, a part of the same rank: a part imports only a strictly lower-ranked part or `driver_base`. ...']
(b) ninth row, L5: ['exceptions row Driver.__init__ -> UNTIL_PAST (name) no longer occurs as an upward edge: ...', 'the map: exceptions row Driver.__init__>UNTIL_PAST>name is new: the list is pinned and shrink-only, ...']
(b) ninth row, pin_problems: ['copy: exceptions row Driver.__init__>UNTIL_PAST>name is new: ...']
(b) deleted row Driver.close_window_series Driver.window_key
(b) deleted row, pin_problems: ['copy: the pin holds the row Driver.close_window_series>Driver.window_key>call but the map no longer does: drop it from PINNED_EXCEPTIONS in this commit ...']
(b) control, unmutated copy: []
(c) L11: ['story_run.py:9 calls module_facade.install but family.installed is false: ...', 'story_run.py:2 imports module_facade but family.installed is false: ...']
```

## Family names in check code (case-insensitive `story_run|driver_|Driver`, fixtures from `BASE_SOURCE` on excluded)

- l.1-25 module docstring and usage lines: comments/docs naming the first family and the file.
- l.45 comment "driver-only tables".
- l.60-68: the pin data (`story_run` key and 8 rows).
- l.111, 432, 643, 652-655, 715: `not_driver`, the NAME of an existing map key (schema key, in the map; renaming it changes `not_driver` rows, which are outside the non-goals); 715 is a comment. Reported, not changed.
- Nothing else in check code; `real_maps`/`main` hold none.

## FR walk (section G)

FR-29: no heredoc, no escape bytes (the BOM fixture is built with `chr(0xFEFF)`); no control byte (checked). FR-30: English/ASCII only (checked: 0 non-ASCII). FR-31: no load-dependent test (temp dirs, no timing). FR-32: each fix has its refusal fixture and the green run above. FR-33: n/a (a test, not a role change). FR-34: n/a. FR-43/44/45: no process, no new doc location, the validators write nothing outside temp dirs. FR-47: n/a. FR-52: n/a. FR-54: siblings listed below. Sections A-F: no refusal text to a person or role contract changed beyond problem texts that name what is wrong, what is expected, and the door (FR-1).

## Decisions I took inside the spec, and questions

1. "Class tables" on `class: null` (decision 7) is not defined in the dispatch. I took `attributes`, `state_keys`, `dynamic_state_keys`, `string_dispatch` (the four that describe `self`); `adhoc_attributes` (Person) and `stdout_writers` stay legal. Constant `CLASS_TABLES`. Lead: confirm or widen.
2. B1 "when it cannot run it says why in one line": after L10 passes the clause always runs, so there is no such case and no line is printed.
3. `l12_class_use` in a part refuses the assembled class only; a mixin name of ANOTHER part's home (not "its own") is still accepted by the existing home rule (decision 9 as written, F7 (i)). Tightening to "own mixin or Base only" is a further step; not taken.

## Real tree

No red on decisions 1, 7, 9 and the new L11/E8 checks: `driver_chains` and `driver_timing` import no family module and do not touch `Driver.` by name; no script imports module_facade today.

## Analogs noticed (not fixed, FR-54 / rule 5)

- `prefix` is globbed as-is (`scripts/<prefix>*.py`); a prefix with a path separator or glob character is not refused by L10 (same class as the facade path case).
- `not_driver` is a family-named key in the map schema (AR-1); a neutral name would be a map-wide rename.
- Critic queue lines 1-7 stay with the Lead as written.

## Needed beyond the manifest

`scripts/tests/harness.py` (FIXTURES, temp_dir) and `scripts/module_facade.py` existence; the live map's `exceptions` rows.
