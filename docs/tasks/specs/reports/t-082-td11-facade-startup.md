# t-082 -- the facade's start-up cost (module_facade.install compiled every part a second time)

Owns changed (worktree `agent-a7794056795e8efa6`, nothing committed): `ai-packages/qa-factory/scripts/module_facade.py`,
`ai-packages/qa-factory/scripts/tests/test_module_facade.py`, this report. Scratch scripts (outside the repo, in the
session scratchpad): `inst_time.py`, `help_time.py`, `equiv.py`, `oldscan.py`, `equiv_names2.py`, `neg.py`.

## 1. Timing BEFORE / AFTER (this machine, `python -B`, 3.12.10)

| measure | BEFORE | AFTER |
|---|---|---|
| (a) `-X importtime`, cumulative of `story_run` (self) | 1534821 us (self 561333 us) | 950301 us (self 9852 us) |
| (a) `module_facade` import line | 2028 us | 2632 us (the file is longer; noise) |
| (b) mean of 10 runs `story_run.py --help` | 1.584 s (1.57-1.61) | 0.987 s (0.96-1.06) |
| (c) `perf_counter` around `install` on a stand-in over the 17 real parts | 0.540 s, 0.560 s | 0.0071 s, 0.0070 s |

Before-the-cut cost cannot be measured (uncut tree gone): absolute numbers only. The rest of the 0.95 s is the driver's
own imports (`controller` 190 ms self, `gate_preflight` 112 ms, `contract` 82 ms, `source_inventory` 41 ms,
`hooklib` 20 ms self), not the facade.

## 2. What changed and why it is equivalent

1. `_code_of` (loader `get_code`, a second compile under `-B`) is gone. New `_live_codes(part)` walks what the import
   ALREADY built, from `part.__dict__`: functions whose `__globals__` is the part's dict; members of classes defined in
   the part (`vars(cls)`, staticmethod/classmethod/bound-method `__func__`, property fget/fset/fdel,
   `functools.partial.func/args/keywords`, `cached_property.func`, any object with `__wrapped__` in its `__dict__`);
   closure cells; defaults/kwdefaults; lists/tuples/sets/dicts at module level (lambdas in a table). Nested functions,
   comprehensions (3.11- as code consts) and class bodies inside functions come through the existing recursion of
   `_scan` over `co_consts`. Seen-set by `id` guards cycles. A module-level callable that none of this reaches (an
   instance with `__call__`, ...) is listed per part in `state.skipped` (`{part name: [names]}`), never an error.
2. ONE scan stays: `_scan(code)`, called per live code object. Its inside changed (needed to reach the 0.08 s target:
   `dis.get_instructions` alone cost 0.23 s over the 872 live code objects): it reads the raw bytes of `co_code`
   for the seven wanted opcodes (`bytes.find`), follows EXTENDED_ARG backwards, and applies the 3.11+ `LOAD_GLOBAL`
   `arg >> 1`. The test compares it with `dis` on every run (rows below), including a code with 300 globals (EXTENDED_ARG).
3. Class-body names: the old module-code scan saw every class attribute and method name as `STORE_NAME`, so they sat in
   the recorded set. The live walk adds the non-dunder keys of `vars(cls)` of the part's classes to keep that.
4. `_prepare` returns a sixth value (`skipped`); `_State.__init__` takes `skipped=None`. The install-time refusal "no source
   loader" is kept as a cheap attribute check (`loader` has `get_code`), no call. Docstring (WRITES paragraph) rewritten.

Why the module's own top-level code is not needed: Python keeps no module code object after import. What the top-level
code ACCESSED at import time is over (a name read at module level cannot be read again later); what it BOUND is the
module's `__dict__`, which `install` already reads (`set(mod.__dict__)` is in the recorded set and is what the mirror
copies). The M2 refusal does not depend on top-level code: a module-level rebinding is `STORE_NAME`, which is not in
`_REBIND_OPS` (old and new alike); only `STORE_GLOBAL`/`DELETE_GLOBAL` inside functions count, and those are in live code.
Not sufficient for: a builtin or an unbound name that ONLY module-level/class-body code reads (class decorators,
`int` as a default argument, annotations) and anything compiled/exec'd after import (not covered before either).
Fallback to loader code: NOT built; no part of the real driver needs it (see the equivalence below, `skipped=[]` for all 17).

## 3. Equivalence on the 17 real parts (`equiv.py`: OLD = dis scan of the loader's module code, NEW = live codes)

Verbatim (rebound sets are equal and empty for all 17; `skipped` empty for all 17):

```
driver_chains        recorded old=  83 new=  78 old-only=['__get__', '__init__', '__module__', '__qualname__', '__set__', 'list', 'property', 'staticmethod'] new-only=['NotImplemented', 'hash', 'super'] | rebound old=[] new=[] | skipped=[]
driver_core          recorded old= 109 new= 102 old-only=['Exception', '__classcell__', '__init__', '__module__', '__new__', '__qualname__', 'chr', 'range', 'staticmethod'] new-only=['NotImplemented', 'hash'] | rebound old=[] new=[] | skipped=[]
driver_timing        recorded old=  60 new=  55 old-only=['__enter__', '__exit__', '__init__', '__module__', '__qualname__'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_runner        recorded old= 120 new= 117 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_dialog        recorded old=  94 new=  90 old-only=['__module__', '__qualname__', 'classmethod', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_conductor     recorded old= 105 new= 100 old-only=['__classcell__', '__init__', '__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_dispatch      recorded old= 253 new= 247 old-only=['__module__', '__qualname__', '_rp', 'classmethod', 'object', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_s0            recorded old= 156 new= 151 old-only=['__module__', '__qualname__', 'bytes', 'int', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_sources       recorded old=  69 new=  65 old-only=['__module__', '__qualname__', 'int', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_plan    recorded old=  81 new=  78 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_build   recorded old=  50 new=  46 old-only=['__module__', '__qualname__', 'staticmethod', 'tuple'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_s5      recorded old=  55 new=  52 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_s6      recorded old= 126 new= 123 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_s7      recorded old=  79 new=  76 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_stage_s8s9    recorded old=  48 new=  43 old-only=['__module__', '__qualname__', 'bool', 'int', 'tuple'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_gates         recorded old= 106 new= 102 old-only=['__module__', '__qualname__', 'staticmethod', 'tuple'] new-only=[] | rebound old=[] new=[] | skipped=[]
driver_machine       recorded old= 208 new= 215 old-only=['__module__', '__qualname__', 'staticmethod'] new-only=['_asdict', '_field_defaults', '_fields', '_make', '_replace', 'default_stage', 'forms', 'gaps', 'gate', 'rehearsal'] | rebound old=[] new=[] | skipped=[]
```

The sets are NOT strictly equal; every difference, by class, name by name:
- old-only, class-body-only reads/dunders: `__module__ __qualname__ __classcell__ __init__ __new__ __get__ __set__ __enter__ __exit__`
  (class-body `STORE_NAME` of dunders; the dunder filter on class members drops them, no test writes a dunder through a facade);
  builtins read ONLY while a class body or decorator ran: `staticmethod classmethod property list object int bytes tuple bool chr range Exception`;
  `_rp` (a temporary `import runtime_paths as _rp ... del _rp` in a class body of `driver_dispatch`, nowhere else).
  All are "accessed only by top-level code": over after import.
- new-only (an excess, harmless): `NotImplemented hash super` (accessed as globals by dataclass-GENERATED `__eq__`/`__hash__`/`__init__`
  whose `__globals__` is the part: the live walk sees them, the module code could not; the new set is the more faithful one) and
  in `driver_machine` `_asdict _field_defaults _fields _make _replace default_stage forms gaps gate rehearsal`
  (members of a NamedTuple class, generated plus its fields; a patch of such a name would also write a copy into
  `driver_machine`, as the old code did for every class attribute; reads unchanged).
- Search that none of them is written through the facade: Grep over `ai-packages/qa-factory` for
  `(object|setattr|delattr)\(\s*[\w.]+\s*,\s*"<any of the names above>"` -> no matches; for `\b(story_run|SR|_sr|X)\.<name>\s*=[^=]`
  -> no matches; for `"story_run.<name>"` (patch string form) -> no matches. Positive controls with the same shapes on
  known names (`_now`, `open`, `time`, `boundary_step`; `story_run._now =`, `.time =`, `.json_record`) -> 2 files / 3 files found.
  The names tests do write through `story_run` (aliases `story_run`): `Driver EXIT_INFRA _now _read_jsonl _write_json json_record open time` --
  none is in the difference list (all are module-level names or builtins read in functions: recorded both ways).
  Limit of this search: a receiver under another alias than `story_run SR _sr X` in a `x.name = v` form is not covered by the
  third grep; the first grep takes any receiver for the patch/setattr forms.

## 4. Tests (`test_module_facade.py`, was 97 checks, now 124)

New rows: `recorded set equals the loader-code set` (fixture with nested function, comprehension, classmethod, staticmethod,
property, decorated function with `functools.wraps`, partial, lambda in a table, `global` store in a method; compares with an
independent `dis` scan of the compiled source; allowed old-only = import-time names, new-only = empty; a patch of a name only a
table lambda reads lands in that part and leaves no trace); `install compiles nothing a second time` (counting `SourceFileLoader.get_code`:
the import asks, `install` asks nothing); `a part of constants only`; `a callable object is skipped, not an error` (`skipped == {"sk_a": ["obj"]}`);
`the fast scan equals dis` (300 globals / EXTENDED_ARG, the fixture, module_facade.py, the test file; accesses and rebinds; attribute-only name not recorded);
`global in a method or nested function is refused` (M2 refusal reaches both). Fallback row: none (no fallback built).

## 5. Negative controls (byte copies in the scratchpad, `neg.py`; each mutated file differs by hash, `mutated=True`)

```
## M-1 control (no mutation): mutated=False exit=0      === test_module_facade: 124/124 ok ===
## M0 shadow restore disabled: mutated=True exit=1
    FAIL two parts, different objects, restored per place: each part has ITS OWN original back
    FAIL a part that only reads a name gets no binding: after the block that part has no binding
    FAIL del then restore of two objects: each part has ITS OWN object back
    === test_module_facade: 121/124 ok ===
## M1 mirror removed: mutated=True exit=1
    FAIL live read of a part global: documented limit: a direct write into a part bypasses the facade, the mirrored copy is stale
    FAIL assign seen by the defining part: row raised ...   (+ patch_part_only_name, module identity kept, ... ) failing rows: 9
## M2 recorded widened to all co_names: mutated=True exit=1
    FAIL recorded set equals the loader-code set: nothing is recorded that the loader code does not show -- ['wraps']
    FAIL the fast scan equals dis ... accesses -- ['attr'] / ['partial','wraps'] / [...]   failing rows: 8
## M3 facade-own place dropped: mutated=True exit=1
    FAIL builtin patch reaches facade code: a patch reaches the facade's own code and the part that also reads it
    FAIL builtin patch reaches facade code: an assignment reaches both
    === test_module_facade: 122/124 ok ===
```

M2 note: the old test table did not catch "recorded widened to all co_names" by name alone; here the new rows catch it
(the earlier verdict's M2 refusal control is the row `global in a method ...` plus the scan-equals-dis rows).

## 6. Verbatim DoD output

```
python -B .../tests/test_module_facade.py            === test_module_facade: 124/124 ok ===
python -B .../tests/test_story_run_words.py          === test_story_run_words: 115/115 ok ===
python -B .../tests/test_driver_chain.py             === test_driver_chain: 170/170 ok ===
python -B .../tests/test_judgment_census.py          === judgment_census: 22/22 ok ===
python -m pyflakes <two files>                       (no output, exit 0)
git status --porcelain                                M ai-packages/qa-factory/scripts/module_facade.py
                                                       M ai-packages/qa-factory/scripts/tests/test_module_facade.py
                                                      (+ this report, new)
```

The census unit holding `raise ValueError` (`_prepare`, `install`) is not moved or renamed; its row needs no edit.

## 7. FR walk (section G, the only one touched; `module_facade.py` is package code)

- A/B/C/D/E/F: no refusal text, human text, contract or report changed (the existing refusal texts are byte-identical but for none).
- FR-29: no escape sequences via heredoc, no control byte; files written with the Edit/Write tools.
- FR-30: English/ASCII only (grep-free check: no Cyrillic typed).
- FR-31: no timing-dependent assertion added (the 0.08 s target is in this report, not in a test).
- FR-32: root cause (second compile + `dis` object per instruction), with tests; the full selftest is CI's.
- FR-45: the walk writes nothing (reads only `vars`, `__code__`, closures).
- FR-47/AR-15/AR-14: one survivor kept; `_scan` is the single scan; AR-7 not touched. AR-n touched: AR-15 (one facade for every cut file), AR-20 n/a.

## 9. Round 2: critic fixes F1, F2, F4 (t-083)

- F1: `_scan_dis` is now in `module_facade.py` (the old body; the test's `dis_scan` is an alias to it, one copy). `_scan` compares
  `_scan_fast` with `_scan_dis` once per process on `_PROBE` (300 names, a function with `global`/`del` and a comprehension,
  a class body); mismatch or any exception -> `_fast_ok = False` and `_scan_dis` for the process; any exception on one code
  object -> `_scan_dis` for that object. New row `fast scan is active` (`_fast_ok is True`, the probe agrees, a failing fast
  road turns the process to `dis`); the equality row now compares `_scan_fast` itself (not masked by the fallback) and `_scan`.
- F2: `_has_global_statement(part)` (source bytes of `spec.origin` against `(?m)^\s*global\s`; unreadable source counts as a hit)
  -> that part's rebound set comes from `_scan(loader code)`; recorded sets still come from the live walk. Zero cost for the
  17 driver parts (0 hits). Rows: `global in unreachable code is refused` (instance-attribute shape; control: the walk alone does
  not reach the function), and the no-second-compile row now shows a `global`-free part asks the loader for nothing and a `global`
  part asks for exactly itself. Docstring: NOT COVERED line added, plus the qualified "nothing is compiled a second time".
- F4: the variable is `members`.
- Your open questions: class-body names kept; instance dicts not walked.

Results:
```
install seconds 0.0184 / 0.018        (stand-in over the 17 real parts; was 0.0071 before round 2: probe + 17 source reads)
mean help 0.982 [0.98 ... 1.03]       (10 runs of python -B story_run.py --help)
=== test_module_facade: 134/134 ok ===
=== test_story_run_words: 115/115 ok ===
=== test_driver_chain: 170/170 ok ===
=== judgment_census: 22/22 ok ===
pyflakes on both files: exit 0
git status --porcelain: M module_facade.py, M tests/test_module_facade.py, ?? this report (owned paths only)
```
Negative controls (byte copies, `neg.py`; control 134/134):
```
M0 shadow restore disabled           3 rows red (131/134)
M1 mirror removed                    9 rows red
M2 recorded widened to all co_names  6 rows red (scan-equals-dis x4, "fast scan is active: ... -- False", "the probe itself agrees")
M3 facade-own place dropped          2 rows red (132/134)
M4 probe comparison disabled (_fast_ok = True) AND fast scan broken (_GLOBAL_ARG_SHIFTED flipped): 6+ rows red:
    FAIL recorded set equals the loader-code set: nothing is recorded that the loader code does not show -- ['wraps']
    FAIL the fast scan equals dis: row raised ...
    FAIL fast scan is active: the probe itself agrees
    FAIL fast scan is active: a failing fast road turns the process to dis
M5 (extra) F2 road dropped           2 rows red: "a part with a `global` line is read through the loader", "global in unreachable code is refused"
```
The census unit holding `raise ValueError` (`_prepare`, `install`) was not moved; the `_prepare` body grew (a call to `_has_global_statement`/`_loader_code`),
no new `raise ValueError` unit.

## 8. Questions / noticed (not decided)

1. Class members walk added (item 3) keeps old class-attribute names in the recorded set. They are not module globals, so a
   stricter design would drop them (old behaviour: junk copies of written names land in a part dict). Kept for equality; Lead may prefer to drop it (then ~900 old-only names, all class attributes).
2. Instances' `__dict__` are not walked (a lambda stored only on a module-level instance attribute is unreachable and not listed in `skipped`). None in the real driver.
3. Needed beyond the manifest: `story_run.py` header, `driver_dispatch.py` around line 2267, grep over `scripts/tests` for facade writes.
4. Analog (same class, not touched): other import cost of `story_run` (`controller`, `gate_preflight`, `contract`, `source_inventory`) is 0.7 s of the 0.95 s; any other user of `module_facade.install` pays the same (`test_driver_layers.py` uses it; only story_run installs it in the package).
