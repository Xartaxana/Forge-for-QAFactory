# t-047 attempt 2 / TD-11 node B0a -- fix round for module_facade.py (builder report)

Files changed in WT (`C:\QAFactory\forge-repo\.claude\worktrees\agent-a70cb266381a52ce9`), no commit:
- `ai-packages/qa-factory/scripts/module_facade.py` (now 249 lines; no function over 60 lines)
- `ai-packages/qa-factory/scripts/tests/test_module_facade.py` (97 PASS lines, was 62)

Structure change (forced by the 60-line limit): the closures of `install` became `_State` (read_now, part_value, forward,
write, delete, restore, still_ours) plus a per-install `_Facade` subclass carrying `__module_facade_state__`; `install`
itself is ~15 lines; `_prepare` validates/scans without touching the module.

## Findings, one line each

- B1 fixed: at install every non-machinery name a part binds is mirrored into the facade dict (first part wins, a facade's own
  binding stays), except names ANY part rebinds through STORE_GLOBAL/DELETE_GLOBAL; mock sees them as local. Rows:
  `create=True on an existing part name`, `builtin-named part binding patched`, `reader thread during patch enter/exit`.
  Literal-`del` semantics unchanged (rows `builtin_open_through_the_facade`, `del then restore of two objects`).
- M1 fixed: `_scan` records only opnames LOAD/STORE/DELETE_GLOBAL, LOAD/STORE/DELETE_NAME, LOAD_FROM_DICT_OR_GLOBALS (taken
  from `dis.opmap`, so only where the Python has it) over every nested code object; plus the names in the part's dict. A
  forwarded read goes to the install-time home part first. Rows: `global cache read live, earlier part mentions it`,
  `a part that only reads a name gets no binding` (attribute-only part gets no binding).
- M2 fixed: `_prepare` raises ValueError naming the name, the rebinding part and the other place (facade or part) when a
  STORE_GLOBAL name is also bound elsewhere; runs before the class swap and before any mirror. Row
  `global-rebound copy refused at install` (copy in the facade, copy in a second part; module stays a plain `ModuleType`
  with its dict unchanged).
- M3 fixed: the facade's own global-access names are scanned from `sys._getframe(1).f_code` and are a write place (-1); the
  shadow restores/removes it. Row `builtin patch reaches facade code` (patch via patch.object, assign, del; passes when run
  as `__main__` too: row `facade run as __main__` unchanged and green, directly and through run_py_entry.py).
- m1 `RLock`: row `re-entrant write finishes`. m2 `delete` records a shadow when none exists: row
  `del then restore of two objects` (the monkeypatch.delattr shape: getattr, delattr, setattr). m4 message says reload of a
  facade is not supported. m5 not done. Docstring builtin sentence fixed; `list(holders)`.
- M4 rows: all ten requested are present by name (list in the ROWS table, last 11 entries; plus `empty parts` for the edge).
- Deviation (trivial): the comment "why `__getattr__` repeats the loop of `read_now`" is moot: the loop now lives once in
  `_State.part_value`, used by both `forward` and `read_now` (home-first read must be identical in both).
- Edits to existing rows forced by F1 (mirroring): `live read of a part global` (a direct `part.X = 4` is now asserted as the
  documented stale limit), `assign seen by the defining part`, `patch_part_only_name`, `module identity kept` (the facade dict
  now holds mirrored names).

## DoD witness (verbatim)

Command: `python -B C:\QAFactory\forge-repo\.claude\worktrees\agent-a70cb266381a52ce9\ai-packages\qa-factory\scripts\tests\test_module_facade.py`
```
=== test_module_facade: 97/97 ok ===
```
(0 FAIL lines; first run after the code change showed exactly the 4 expected failures from F1, listed above, fixed.)

### Negative controls (BYTE COPIES in a temp tree, script `...\scratchpad\neg47\run_neg.py`, worktree file never touched)
```
## N0 unchanged: exit 0 ['=== test_module_facade: 97/97 ok ===']
## a shadow restore disabled: exit 1 ['=== test_module_facade: 94/97 ok ===']
    FAIL two parts, different objects, restored per place: each part has ITS OWN original back
    FAIL a part that only reads a name gets no binding: after the block that part has no binding
    FAIL del then restore of two objects: each part has ITS OWN object back
## b mirror step removed: exit 1 ['=== test_module_facade: 84/94 ok ===']
    FAIL live read of a part global: documented limit: a direct write into a part bypasses the facade, the mirrored copy is stale
    FAIL assign seen by the defining part: row raised ...   (also patch_part_only_name, module identity kept, two parts..., create=True..., builtin-named...)
## c recorded = all co_names: exit 1 ['=== test_module_facade: 95/97 ok ===']
    FAIL a part that only reads a name gets no binding: a plain write gives no binding to a part that mentions the name only as an attribute
    FAIL global cache read live, earlier part mentions it: the part ordered first holds no copy
## d facade-own place dropped: exit 1 ['=== test_module_facade: 95/97 ok ===']
    FAIL builtin patch reaches facade code: a patch reaches the facade's own code and the part that also reads it
    FAIL builtin patch reaches facade code: an assignment reaches both
```
Note on (c): the live-READ line of row `global cache read live...` stays green under (c) because the home-part-first read
masks the stale copy (defence in depth); the row still goes red on the "holds no copy" line.

### Read cost (`python -B ...\scratchpad\neg47\bench.py`, timeit, min of 5 x 1e6)
```
mirrored name f.Y: 0.069 s per 1e6 reads
forwarded (global-rebound) name f.CACHE: 0.843 s per 1e6 reads
```
(about 0.07 us and 0.84 us per read.)

Other checks: file lines 249 / 420; non-ASCII chars in both files: 0; `scenario_walk.py --witness-for scripts/module_facade.py`
still prints "no scenario or keep row covers ..." (expected, keep row not yet landed).

## FR walk (section G; others)
- A-F: not touched (plumbing; ValueError/AttributeError for code callers). FR-29: Write tool, ASCII, no control bytes.
  FR-30: English/ASCII (0 non-ASCII). FR-31: the thread rows use bounded joins and no timing assertions (the reader row can
  only miss a race, never fail falsely). FR-32: root causes fixed (B1 by mirroring, not by a symptom patch). FR-33/34: n/a.
  FR-43/44/45: n/a. FR-47: no judgment, plumbing. FR-52: n/a. FR-54: single survivor (AR-15); AR-13 kept for reads.
- Siblings noticed (not done, report only): spec E3 and the move tool's R12 should state "a bare reader of a global-rebound
  name shares its part or reads through the facade" (critic M2 proposal) -- queue on the B-tool node, Lead decides.

## Ready blocks

Keep row for `scripts/tests/test-layers.json` (unchanged from the first report):
```
  "test_module_facade.py": {
   "layer": "table",
   "why": "table (B.2 criterion 5): the forwarding facade, read/write/patch/main/dir rows",
   "covers": [
    "module_facade.py",
    "run_py_entry.py",
    "tests/harness.py"
   ]
  },
```
Judgment census: NOT run. The only unit holding a literal `raise ValueError(` is `_prepare` (`_code_of` and `install` hold none
now; grep of the file lines 101-129 shows all 7 sites inside `_prepare`). ONE row (roles guessed empty; verify with
`test_judgment_census.py` after the file lands):
```
{"file": "module_facade.py", "function": "_prepare", "class": "shape", "roles": [], "owner": "data"}
```
If the census reads nested/other units differently, the candidates are `install` (no raise now) and `_code_of` (no raise now): no
row for them.

## Questions
None. Needed beyond the manifest: harness.py glob and `run_py_entry.py` (to build the control copies), `refusal_registry.py`
(REFUSAL_RAISES = StateConflict/ValueError, to place the census row).
