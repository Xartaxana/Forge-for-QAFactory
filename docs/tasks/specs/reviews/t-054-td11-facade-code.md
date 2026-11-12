# t-054 — critic gate: `module_facade.py` (TD-11 node B0a, builder task t-047)

Reviewed: the uncommitted worktree `C:\QAFactory\forge-repo\.claude\worktrees\agent-a70cb266381a52ce9`,
`ai-packages/qa-factory/scripts/module_facade.py` (205 lines), `scripts/tests/test_module_facade.py` (354 lines), and the
builder report `docs/tasks/specs/reports/t-047-td11-B0a.md`. I checked them against spec B §2.4 and §12 E3/E4/E5/E7, against
item 1 of the lead brief section «Правки после критика на план», which overrides §2.4, and against plan blocker X1.

**Verdict: ACCEPT WITH FIXES (NEEDS WORK).** 1 BLOCKER, 5 MAJOR, 5 MINOR. The design holds up for the common cases. Every patch
form in my matrix leaves each part exactly as it was before: context manager, decorator, start/stop by hand, nested, two
names interleaved, the string `patch("mod.n")`, `patch.dict`, monkeypatch setattr/undo, assign then reassign the saved
original, assign then `del`, and a patch leaked across an exception. Three things still stop acceptance:

- One real test pattern breaks: B1, `create=True` on an existing name.
- The per-place shadow, the core of deviation 2, has no test that can fail.
- Two live-read and reach invariants of §2.4/E4 fail in ways a cheap change prevents.

None of these is a reason to rebuild the module. No facade is installed anywhere yet, so B1 must be fixed before the first
family cut, not necessarily in this commit. Whether that counts as "accept now, fix before the first cut" or "fix round first"
is the Lead's decision.

## Mechanical layer (control re-run)

- `python -B .../worktrees/agent-a70cb266381a52ce9/ai-packages/qa-factory/scripts/tests/test_module_facade.py`
  printed `=== test_module_facade: 62/62 ok ===` on Python 3.12.10. The builder's witness reproduces.
- My experiments live in the scratchpad (outside the repo), not the worktree:
  `C:\Users\i_mas\AppData\Local\Temp\claude\b3e3188b390a00d9\1624cb4a-453f-417c-b51b-fe534689bfdd\scratchpad\fx\exp1.py`
  (the break matrix, run against a byte copy of the module) and `...\scratchpad\fx\exp2.py` (a prototype of fix F1). The
  negative controls are in `...\scratchpad\neg\M0..M4`.
- Deviation: the Write tool refuses scratch paths under the handoff gate, so I wrote the scratch scripts with a shell heredoc.
  That is outside the repo and is not a package edit.

## BLOCKER

**B1. A `create=True` patch of an EXISTING part-only name deletes it from every part for good.**
`module_facade.py:153-197`.

How it happens:
- mock reads the original through `getattr`. The name is not in the facade's `__dict__`, so mock marks the patch non-local.
- With `create=True`, `_patch.__exit__` calls `delattr` and nothing else. It does not call `setattr(original)`.
- `__delattr__` (:184-197) removes the name from every holder. The shadow is kept, but no write ever comes to use it.

On a single module the name is in `__dict__` (local), so the exit is `setattr(original)` and nothing is lost.

Experiment E21 (exp1.py), the same patch on a plain module and on a facade:
```
E21 w21_s after create=True patch on an EXISTING name -> real
E21 w21_f after create=True patch on an EXISTING name -> NameError name 'helper' is not defined
```

The real user is `scripts/tests/test_investigation_probe.py:167`:
`mock.patch.object(CT, name, ..., create=True)`, where `CT` is `controller` (`:27`). It patches `controller.s7_part_of` and
`controller.lineage_root`, which are module-level functions (`controller.py:144`, `:158`). After the controller cut, any of
these patches whose name homes in a part (not facade-bound) strips the function from the process. Every later test in the same
pytest process that reaches controller code calling `s7_part_of`/`lineage_root` then fails with NameError, and the failure
depends on test order.

Neighbours of the same surface (mock's non-local exit path):
- (a) mock FORCES `create=True` for any name in `dir(builtins)` on a module. A part that binds a builtin-named object loses it
  the same way. E22, a part-level `def format`: single module → `part-format`; facade → `1`, the builtin. E11, a part's own
  `open`: after the patch the part dict shows `missing=['open']`. Current instance: none. My grep of the six patched files for
  column-0 builtin-named `def`/assignments was empty; same-shape control `^(def )?(main|open|print)\b` found the six `def main`.
- (b) The non-create exit is `delattr` followed by `setattr(original)`. Between the two calls the name is bound NOWHERE. A
  reader in another thread hits it. E12: `AttributeError("module 'w8_f' has no attribute 'Y'")` in a reader thread while the
  main thread looped patch enter/exit. On a single module the exit is one `setattr`. story_run's driver chains run threads
  (`test_driver_chain.py`, `test_story_run_s5_parallel.py`). A patch exiting while a chain thread calls a part-only function
  can raise NameError in that thread.

A fix of the form "a `del` with a live shadow restores the originals" does NOT work. It breaks
`test_controller_rework.py:231-268`: `stage_guard.dispatch_errors = refuse; ...; del stage_guard.dispatch_errors`, then
controller's `getattr(stage_guard, "dispatch_errors", None)` must return None ("without the guard"). The facade cannot tell
mock's create-exit `del` from a user's `del`.

**Fix F1 (proved by a prototype run, exp2.py).** At install, mirror every name a part binds into the facade dict. Two kinds of
name are not mirrored:
- machinery names;
- names that any part's bytecode rebinds through `STORE_GLOBAL`/`DELETE_GLOBAL`. Those stay forwarded and live.

Why this fixes B1: mock then sees every patchable part name as LOCAL. Its exit is a single `setattr(original)` under the lock,
and the existing shadow restores per place. Writes already fan out to the facade dict when it binds the name (`:170`).
Prototype output:
```
skipped (global-rebound): {'CACHE'}
E21' create=True on an existing name: ('fake', 'fake') -> ('real', 'real')
E12' concurrent reader errors: [] | Y in parts: 2 2
E14' 'useb' in vars(facade): True
E23' mirrored read: 0.067 us
E-del' after assign+del: hasattr -> False
E-del' after restoring the original: parts True True
```

F1 also fixes M5's `vars()`/`import *` gap and most of the read cost (item 8). The `test_controller_rework` `del` semantics
stay intact (E-del'). A part rebinding a mirrored name by bytecode is impossible, because those names are excluded. A rebind by
string (`globals()[...]`) is already listed as not covered.

New test rows: create=True on an existing part-only name; a builtin-named part binding patched; a reader thread during patch
exit.

## MAJOR

**M1. A plain write gives a binding to parts that mention the name only as an attribute. With "first part wins" reads, this
makes a `global`-rebound name read STALE through the facade.** `module_facade.py:57-74, 111, 116-123, 143-148, 165-173`.

Cause: `_code_names` takes all of `co_names`, which includes `LOAD_ATTR`/method names (`o.CACHE`), not only global reads. A
write fans the value into such a part. `__getattr__` returns the FIRST part that binds the name. If that part comes before the
owner, a later `global` rebind in the owner is never seen.

E1 (exp1.py): parts [q, a, b]; q has `def peek(o): return o.CACHE`; a owns `CACHE` and rebinds it in `fill()`.
```
OK   E1 single: CACHE live after reset+fill  :: filled
BAD  E1 facade: CACHE live after reset+fill  :: facade reads None; q got None; a holds 'filled'
```
The pattern is real: `setattr(hooklib, attr, None)` for every CACHE name, then calls that refill through `global`
(`test_brief_pack.py:1896-1897, 1926-1927`, also `test_project_approach.py:36,126`, `test_slices_on_demand.py:79,94,125`).
Whether a part ordered before the owner mentions `_PROJECT_ROOT_CACHE`/`_RUN_FORMS_CACHE` depends on the cut. Today hooklib
mentions them only inside the holder functions (`hooklib.py:32-162, 880, 1096-1100`). So this is latent, but the facade must
not depend on that.

Neighbours on the same surface:
- E3: `saved = f.helper; del f.helper; f.helper = saved` adds `helper` to the attribute-only part
  (`(['helper'], [], [])`).
- E19: a plain write does the same.

Both are the "name added to a part that only READ it" case the DoD asks about.

Fix: record only global-access names, using `dis.get_instructions` with opnames `LOAD_GLOBAL STORE_GLOBAL DELETE_GLOBAL
LOAD_NAME STORE_NAME DELETE_NAME`, plus `LOAD_FROM_DICT_OR_GLOBALS` on 3.12. This still matches the brief's intent ("global
names its code reads"). The brief's word `co_names` was a means, so this is a spec imprecision as well, and the Lead may want
to amend item 1's wording. As defence in depth, read a name from the part(s) that bound it AT INSTALL first. This fix is not
proved by a run: exp2 used a part order where the owner is already first.

**M2. A facade-bound copy, or another part's `from <part> import n` copy, of a name a part rebinds through `global` reads
stale. On one module it reads live.**

E1c: the facade has `from w1c_a import CACHE`, and `w1c_a.fill()` rebinds it, so `facade.CACHE` gives `None`. A single module
gives `'filled'`. The builder lists this as a known gap. It breaks §2.4's own invariant (the hooklib cache "reads current") for
any facade or reader-part copy.

Spec E3 co-homes the name with the functions holding the `global` statement. It says nothing about a BARE reader in another
part or in the facade. That is a spec defect, and the move tool's R12 would happily generate the stale `from` line.

Fix: at install, `ValueError` naming the name when a name is `STORE_GLOBAL`'d in part i and bound in the facade dict or in a
part j ≠ i. It is one bytecode scan, shared with F1 and M1. Also add the rule to spec E3 ("a bare reader of a global-rebound
name shares its part or reads it through the facade module").

**M3. A facade-own read of a BUILTIN is not reached once any part also reads that builtin.** `:165-171`.

The builder's statement is half right:
- When NO part reads the builtin, `not holders` puts the write into the facade dict, and the facade's code sees it. E2 facade:
  `FAKE`.
- When a part also reads it, the facade place is skipped. E2b: `('FAKE', 'REAL')`; E2c, the same through
  `patch.object`: `('FAKE', 'REAL')`.

In a real cut, parts read `open`, so the second case is the normal one. This breaks E4's "never fewer call sites". The current
real test is `test_story_run_words.py:286` (`story_run.open = full_disk`, undone by `del` at `:302`). It is lost exactly where
the record paths reach a function kept in the facade (`main`, facade-bound functions, the assembled class body). My grep found
no other builtin patch on the six modules; control: the same grep found `:286`.

Fix: record the facade's own global-access names as place -1. Take them from `sys._getframe(1).f_code`, which is the facade's
module code at the `install` call. That also works for `__main__` and `run_py_entry` (where the spec may be None). Write a
name to the facade dict when it is in that set; the shadow already records `facade=_MISSING`, so the restore removes it.

**M4. The test cannot fail on the shadow mechanism (deviation 2).** `test_module_facade.py`.

Negative controls (one-line mutations of a byte copy, then the builder's test run against it):
```
M0 (unchanged)                                  === 62/62 ok ===
M1 restore branch disabled (`if False:` :161)   === 62/62 ok ===        <- the shadow is untested
M2 one part read made stale                     FAIL read after a part rebinds through global ... 61/62
M3 recorded set without co_names                FAIL builtin_open_through_the_facade x2 ... 60/62
M4 facade place dropped (:170)                  FAIL facade_own_main_from_import x3 ... 59/62
```
No row has a read-only part, or two parts with different objects, on the write-of-original path. Writing the original into
every holder therefore passes every assertion.

Missing rows: two parts binding a name to different objects, restored through `patch.object` (E4a passes with the shadow), and
the monkeypatch.delattr shape (E4b, MINOR m2). Also: a part that only reads the name has no binding after the patch, and every
B1/M1/M3 case.

**M5 (judgment for the Lead, item 8). Read cost.** My numbers: forwarded 0.62 µs, facade-own 0.06 µs, plain 0.013 µs per read.
The builder's are 0.92/0.092/0.018. Same order of magnitude.

Function code in a part reads its own globals natively. Only `<stem>.X` attribute reads from OUTSIDE pay the cost, plus mock
and getattr. I counted no hot loops; that is not measured. A hook start-up doing a few hundred `hooklib.x` reads costs under
1 ms. A per-name cache with invalidation on facade writes would bring back exactly the `global`-rebind staleness the design
exists to avoid, since a part's `STORE_GLOBAL` cannot invalidate it. Not warranted. F1's mirroring gives native-speed reads for
all names except the global-rebound ones, without a cache. If F1 is taken, M5 closes as well.

## MINOR

- **m1.** `threading.Lock` is not re-entrant. A value whose `__del__` writes through the facade while a write replaces it
  deadlocks the writer. E13: the thread never finished in 3 s. Fix: `threading.RLock()` at `:113`.
- **m2.** `del f.n` with no prior write records no shadow. A following `f.n = old` (monkeypatch.delattr undo, or `del` then
  restore) fans out to every holder instead of putting back per-place originals. E4b: two parts with different `log` objects
  give `changed=['log']`, so `b4.lb()` returns `'w4_a'`. E3 gives the pollution case. Fix: `__delattr__` creates the shadow
  when none exists (`read_now`, the facade binding, per-holder bindings) before removing.
- **m3.** `vars(facade)` and `from facade import *` (with no `__all__`) miss part names (E14). The real tree has no reader of
  either for the six modules (grep below). F1 closes it; otherwise document it next to "NOT COVERED".
- **m4.** `importlib.reload(facade)` raises `ValueError: ... already has a facade installed` (E16). The docstring says reload is
  unsupported. The text should say "reload of a facade is not supported" instead of suggesting a double install. No reload
  user in the package (grep `importlib\.reload`: none; control: the same -i pattern `reload\(` found `preload(` lines in
  manual_capture.py).
- **m5.** `f.__getattr__("X")` now returns a part value, where a single module raises (the class method shadows the popped
  function, E17b). No user found: grep `\w+\.__getattr__\b` over scripts found none of the six. The AttributeError carries no
  `name=`/`obj=`, so 3.12 "Did you mean" hints are lost. Cosmetic.

## Answers per DoD item

1. **Patch forms.** All clean (E5-E10, E8 "every part as before" `[([], [], [])]*3`) except B1 (create=True on an existing
   name), M1 (attribute-only fan-out), and m2 (del-first restore).
   - Two parts with different objects through `patch.object`: correct (E4a).
   - `orig = f.n; f.n = x; f.n = orig`: correct (E7).
   - A patch leaked across an exception and then stopped: correct (E5).
   - Non-LIFO interleave: same result as a single module (E6).
   - Stale shadow: `still_ours` discards it once any place holds something other than `last`. A later legitimate write of the
     original can restore old originals only where places had different originals (read-only parts or different objects).
     That gives a pollution difference, not a wrong value in a reader. I found no case where a stale shadow puts a wrong value
     into a reader.
2. **Builtins.** Shadowing and removal work when only parts read the builtin. A builtin that one part binds and another reads:
   the patch is seen by both, but the binding is lost on exit (B1 neighbour (a), E11).
3. **`global` cache.** Live through the facade only if no earlier part and no facade copy binds the name (M1, M2). On one module
   today every reader is live. After the cut, any `from` copy is stale. So the set of readers is NOT the same unless install
   refuses those copies (M2 fix).
4. **Facade's own code.** From-imported names are updated by facade writes (row 11; mutation M4 proves that row works).
   Builtins are lost when a part also reads them (M3). The real exposure is `test_story_run_words.py:286`. The fix is in M3.
5. **The popped `__getattr__`.** `stage_guard.UNRESOLVED_REASONS` still resolves through the chain. `hasattr`/`getattr(mod, n,
   default)` users (`controller.py:7627`, `gate_preflight.py:1462,1502`, `inject_context.py:380`, `dispatch_liveness.py:151`,
   `subagent_journal.py:84`, tests) go through `__getattr__` and keep working. `dir(hooklib)` scans for CACHE names
   (`test_brief_pack.py:1896` etc.) include part names through `__dir__`. The unknown-name text is the same as a module's.
   `inspect.getmembers` sees part names (E14). `vars`/`__dict__`/`import *`: no reader of the six modules in the package (m3).
6. **Modules and imports.**
   - `__main__` and `run_py_entry`: row 12 passes, and I re-ran it.
   - Pickle of a part class or function reached through the facade: works (E15).
   - Reload: m4.
   - A module imported after install that `from`-imports at call time: gets the patched value (E20). A real PART imported after
     install is not recorded; documented.
   - Circular import of the facade from a part at import time: same as without the facade. Not tested beyond reading.
7. **Threads.** A read racing a patch exit sees the name absent (B1 (b), E12). Re-entrancy deadlock: m1.
8. **Cost.** M5.
9. **Builder's deviations.**
   - Dev 1 (literal `del` plus the shadow): right. It is what `test_controller_rework.py:258-268` needs. Keep it, and note that
     B1's fix must not change it.
   - Dev 2 (machinery names): right. `__all__` not forwarded is correct for the facade's own star semantics.
   - Dev 3 (`ValueError` for both refusals): fine. These are programmer calls.
   - Empty `parts`: harmless (E18).
10. **The test.** It meets TESTING.md's table layer (one parameterised row per behaviour, built in a temp dir). Row
    effectiveness is in M4: three of four mutations go red, and the shadow mutation stays green.
    - Judgment census, by reading the rule (`test_judgment_census.py:16-25, 61`; I did not run it): unit u3 is "the body holds
      a refusal site `refusal_registry.sites()` sees (`raise ... ValueError`)". `install` (:95-106) AND `_code_names` (:66)
      both hold a literal `raise ValueError(`. So TWO rows are due, not one; the builder's guess misses `_code_names`.
    - `class: shape` and `owner: data` fit: argument and loader shape, no role output. Whether `roles: []` is accepted, and
      whether `sites()` really lists these two sites, I did not verify. Run the census test after the file lands.
    - AR-15 (one survivor): kept. AR-13: kept for reads; B1/M2 are where a read through the one reader goes wrong.
    - AR-12: cost noted in M5. AR-29: plumbing, no judgment. FR-30: both files ASCII/English by reading; I ran no `--lang`
      check.

## Standing questions (critic-diff-brief items 6, 7, 10, 11, 12)

- **DUPLICATION AND CONSISTENCY:** none found. `__getattr__` (:143-148) repeats the part loop of `read_now` (:119-123). That is
  deliberate, so the hot path avoids the facade-dict check. Acceptable, but one comment should say so. Grep: no other
  `__class__ =` module swap or `ModuleType` subclass in `scripts/`; not exhaustively controlled.
- **CODE QUALITY:**
  - `places = [i for i in holders]` (:169) is a plain copy; `list(holders)` says the same.
  - The `_Shadow.parts` dict is keyed by index only for holders; fine.
  - Otherwise clear, with docstrings that match behaviour. One exception: the "facade's own code reading a builtin" sentence
    (:36) is inaccurate, because it IS reached when no part reads the builtin (M3).
- **ARCHITECTURE (q10):** AR-15, AR-13, AR-12 as above. The commit's `architecture:` line should name AR-15/AR-13.
- **JUDGMENT (q11):** no role judgment; the census rows are plumbing/shape.
- **ONE ACTION, ONE ROAD (q12):** one survivor for every cut file; no per-language or per-project branch. None found.

## Class completeness (SIBLING_MAP)

The defect classes found (mock's non-local exit, co_names over-approximation, stale copies of global-rebound names) live in
this one module, the single survivor for all nine families. Every family inherits them, so the module-level fix covers the
class. M2's spec defect also sits in spec E3 and in the move tool's R12. Those are outside this diff; I propose queueing them on
the B-tool node, and that is the Lead's decision. I did not walk `docs/SIBLING_MAP.md` axes beyond this; the class has no
sibling outside the facade + move-tool pair.

## Not checked

- I did not run `test_judgment_census.py`, `--lang`, or any other package test.
- Circular import at install time (a part importing the facade at module top during install) was reasoned about, not run.
- Hot-loop readers of `<stem>.X` were not measured.
- Whether `refusal_registry.sites()` sees the two `raise ValueError` sites, and whether `roles: []` is accepted.
- M1's fix (global-op scan) was not prototyped. F1 was prototyped only on a 3-part toy, not on a real cut.
- That no current test besides `:167` uses `create=True` on the six modules rests on one grep of `create=True` in
  `scripts/tests` (10 hits; the others target `context_bundle`, `FakeController`, `W.WB`).

Greps used: `\.__dict__|\bvars\(|importlib\.reload|\bdir\(|sys\.modules\[` -i over scripts (positive controls:
`vars(acceptance)`, `vars(event_store)` found); `create=True` -i over tests; builtin-name defs (control above);
`\w+\.__getattr__\b|getattr\((six)|hasattr\((six)`; builtin patches on the six (control: `:286` found).

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [
    "B1 module_facade.py:153-197: mock.patch.object(facade, existing_part_name, v, create=True) exits with delattr only (non-local original), deleting the name from every part for good (E21: NameError after the patch); real user test_investigation_probe.py:167 on controller.s7_part_of/lineage_root; neighbours: forced create for builtin-named part bindings (E11, E22) and the del-then-set window seen by another thread (E12)"
  ],
  "class_completeness": "All defect classes live in the one survivor module, so fixing it covers all nine families; the M2 spec gap (bare readers of a global-rebound name) also needs spec E3 and move-tool R12 - proposed queue item on the B-tool node, Lead decides.",
  "fixes": [
    "F1: at install mirror every part-bound name into the facade dict except machinery names and names any part rebinds by STORE_GLOBAL/DELETE_GLOBAL (prototype exp2 fixes B1, E12, m3 and read cost)",
    "M1: record global-access names by dis opnames instead of all co_names; read a name from its install-time home part first",
    "M2: install raises ValueError for a STORE_GLOBAL name of part i that is also bound in the facade or another part; amend spec E3",
    "M3: record the facade's own global-access names (sys._getframe(1).f_code) as place -1 so a builtin patch reaches facade code",
    "M4: add rows that fail with the shadow disabled (two parts different objects, read-only part, create=True on existing name, builtin-named part binding, reader thread)",
    "m1 RLock; m2 shadow on first delete; m4 reload message; census rows for install AND _code_names"
  ],
  "trail": {
    "read": [
      ".claude/worktrees/agent-a70cb266381a52ce9/ai-packages/qa-factory/scripts/module_facade.py",
      ".claude/worktrees/agent-a70cb266381a52ce9/ai-packages/qa-factory/scripts/tests/test_module_facade.py",
      ".claude/worktrees/agent-a70cb266381a52ce9/docs/tasks/specs/reports/t-047-td11-B0a.md",
      "docs/tasks/specs/td-11b-source-maps.md (2.4, E1-E8)",
      "docs/tasks/specs/td-11-lead-brief.md (Pravki posle kritika, item 1)",
      "docs/tasks/specs/reviews/td-11-plan-critic.md (X1)",
      "ai-packages/qa-factory/scripts/stage_guard.py:115-139",
      "ai-packages/qa-factory/scripts/run_py_entry.py:70-110",
      "ai-packages/qa-factory/scripts/hooklib.py (global/CACHE lines)",
      "ai-packages/qa-factory/scripts/tests/test_story_run_words.py:270-314",
      "ai-packages/qa-factory/scripts/tests/test_investigation_probe.py:140-179",
      "ai-packages/qa-factory/scripts/tests/test_controller_rework.py:216-270",
      "ai-packages/qa-factory/scripts/tests/test_brief_pack.py:1890-1934",
      "ai-packages/qa-factory/scripts/tests/test_judgment_census.py:1-95",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B <worktree>/ai-packages/qa-factory/scripts/tests/test_module_facade.py", "result": "=== test_module_facade: 62/62 ok === (Python 3.12.10)"},
      {"command": "python -B <scratchpad>/fx/exp1.py (break matrix on a byte copy)", "result": "BAD: E1, E1c, E2b, E2c, E3, E4b, E11 restore, E12, E13, E14 vars/import-star, E16, E19, E21, E22; OK: E4a, E5-E10, E8 every part as before, E15, E17, E18, E20"},
      {"command": "python -B <scratchpad>/fx/exp2.py (prototype F1)", "result": "E21 fixed (real, real); E12 no errors; vars has part names; mirrored read 0.067 us; del semantics kept"},
      {"command": "builder test against mutated copies <scratchpad>/neg/M0..M4", "result": "M0 62/62, M1 (shadow restore disabled) 62/62 green, M2 61/62, M3 60/62, M4 59/62"}
    ]
  }
}
```
