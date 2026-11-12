# t-083 -- critic gate: module_facade start-up (t-082 diff, worktree agent-a7794056795e8efa6)

**Recommendation: (B) land it with two named small changes** (F1, F2 below; F3-F5 are notes). The raw scan is
correct on 3.12, and I proved that on a wide corpus. On every other version it is argued, not proven. If it is wrong, the
driver does not start at all on that version, and F1 turns that outage into a slow path. F2 brings back a property of
the t-054 refusal that the live walk lost without a word.

Verdict: NEEDS WORK (fit_with_fixes). Blocking findings: 0. Fixes: F1 and F2 belong in this round. Taken alone,
neither one blocks unblocking main: the driver's 17 parts have no `global` statement, and CI runs 3.12.

## Answers

### Q1 -- the raw scan, by version

What it rests on: the opcode numbers come from `dis.opmap` (line 80-83), so they are never hard-coded and 3.13's
renumbering cannot break them. `co_code` is the DE-optimised array on every version from 3.11 on (CPython
`_PyCode_GetCode` -> `deopt_code`: specialised forms, `INSTRUMENTED_*` (3.12+) and `ENTER_EXECUTOR` (3.13+) go back to base
opcodes, and the cache units become `CACHE` = 0 with arg 0). `dis.get_instructions(adaptive=False)` reads the SAME bytes,
so the two scans can differ only in DECODING. The decoding has three parts:
- opcode bytes are at the even offsets (wordcode, 3.6+). The cache units are opcode 0, and no wanted opcode is 0, so
  reading two bytes per unit without skipping the caches cannot produce a false hit;
- EXTENDED_ARG is walked backwards from the hit, nearest unit = the next-higher byte (line 101-103). That is correct,
  because EXTENDED_ARG always sits directly before its instruction and a cache unit (0) stops the walk;
- `LOAD_GLOBAL` takes `arg >> 1` from 3.11 on (line 84, 104). `LOAD_NAME/STORE_*/DELETE_*/LOAD_FROM_DICT_OR_GLOBALS` index
  `co_names` directly (the last one exists 3.12+ and drops out through `& set(dis.opmap)`).

| version | status |
|---|---|
| 3.12 (3.12.10 here, CI 3.12.16) | **proven**: the test row, plus my battery: 2910 stdlib modules (764 with EXTENDED_ARG, 290 rebound names), 0 mismatches against `dis`; 0 mismatches after `sys.monitoring.set_local_events` on 9702 code objects; a function run hot (specialised) and run instrumented, adaptive bytes != `co_code`, fast == dis |
| 3.10, 3.11, 3.13, 3.14 | **argued** (above); not run: `py -0p` lists only 3.12 and `AppData/Local/Programs/Python` holds only `Python312` |
| 3.15+ | **unknown**. The package floor is "Python 3.10+" (INSTALL.md:127, qa-story/qa-onboarding/qa-doctor READMEs), with no ceiling and no version check; every workflow pins `"3.12"` (canon.yml:69, forge-check.yml:49/120/165, nightly.yml) |

A caveat that applies to the OLD code too: a future global-access opcode with a new NAME is missed by `dis` and by the
raw scan alike, because `_GLOBAL_OPS` is a name list. The raw scan adds risk in exactly one place, the argument encoding.

### Q2 -- when the scan is wrong in the field

I measured both directions on the real driver (in memory, with `_GLOBAL_ARG_SHIFTED` flipped as the stand-in for a
version that changes the encoding):
- **an index out of range** -> `IndexError` in **664 of the 872** live code objects, raised inside `install`, which runs on
  `import story_run`. **The driver does not start on that Python.** Every role on it sees a traceback from
  `module_facade.py:104`. It is loud, but it is a total outage, for a feature production does not even use (next point).
- **in range but wrong** -> wrong `recorded` sets. Production never writes through the facade. I searched `scripts/*.py` for
  `story_run.<x> =`, `setattr/delattr(story_run`, `del story_run.`: the one hit is the comment at ticket_adapter.py:218. No
  production module imports `story_run` at all. Positive control, same shape: 4 test files hit. So a wrong `recorded`
  degrades only TEST patches through the facade, which stop reaching a part. That shows up as a wrong-green or wrong-red
  test, not as a role-visible fault. A wrong `rebound` (STORE/DELETE_GLOBAL, unshifted arg) would hit the mirror (a stale
  copy in the facade dict) and the install-time refusal. Nobody would notice that in the field.

A guard is worth it (F1). It costs about 3 ms per process (measured: compiling a 300-name probe takes 1.05 ms, fast+dis on
it 1.95 ms; on `_prepare`'s own code 0.75 ms).

### Q3 -- the lazy-`dis` alternative

Confirmed: production never writes or deletes through the facade (the search above). So at install production needs only
the MIRROR, and the mirror needs only `rebound` (the STORE_GLOBAL/DELETE_GLOBAL names). That set can be had without
decoding every code object. Use the raw opcode-byte PRESENCE as a prefilter (`any(op in co_code[::2] for op in
_REBIND_CODES)`), with `dis` decoding only the codes that hit. The prefilter errs only in the safe direction: it reads the
same bytes `dis` reads, so it cannot miss, and a false hit costs one `dis` call. Measured on the 17 parts: 0 hits,
0.0020 s. The recorded sets could then be built with `dis` at the first write: 0.259 s over 1339 code objects, once per
TEST process that patches. The code-object list should be snapshotted at install (the walk takes 0.0024 s), otherwise a
part patched directly before the first facade write changes what gets walked (a `MagicMock` in place of a function is
"skipped").

Judgement: (C) is sound, and in one respect it is cleaner, because production would pay nothing for a test-only feature. It
is also a bigger change (lazy state under the lock, latency at the first write inside a `mock.patch`, one more round)
while main is red. F1 gives the same field safety for about 10 lines. **I recommend (B)**. (C) is a legitimate later
simplification, not a requirement.

### Q4 -- what `_live_codes` misses

Shown in memory with three shapes the loader-code scan saw. In each one a part rebinds `CACHE` through `global` and a
second part binds `CACHE`:

```
instance_attr        loader-code rebound=['CACHE'] -> new install: INSTALLED (refusal missed); skipped={... []}
registry_elsewhere   loader-code rebound=['CACHE'] -> new install: INSTALLED (refusal missed); skipped={... []}
fn_attribute         loader-code rebound=['CACHE'] -> new install: INSTALLED (refusal missed); skipped={... []}
stale mirror: part.CACHE = 2  facade.CACHE = 0  'CACHE' in facade dict: True
```

The three shapes:
- `instance_attr`: a function reachable only as a module-level instance's attribute;
- `registry_elsewhere`: a decorator that registers the function elsewhere and returns something else, so the function is
  not in the part's dict;
- `fn_attribute`: a function hung on another function's attribute.

**So the t-054 install-time refusal and the mirror's exclusion are both weakened, silently**: `skipped` stays empty,
because it lists only callables that cannot be reached. The same misses shrink a WRITE's reach for names read only in such
code, which affects test patches only. Not present today: `grep -E "^\s*global\s"` over `driver_*.py` and `story_run.py`
finds 0 (control: 18 in `scripts/*.py`). The future cut candidates use `global` caches in plain functions
(hooklib.py:71/144/156/1096, guard_pre_tool.py:1799/1823/2351), which ARE reached. So it is latent, and it is F2.

The builder's open questions:
- (1) Class-body names in `recorded`: **keep**. They add junk bindings to a part only for the duration of a patch, the
  shadow restores them to absent, and a name the part reads as a global is recorded anyway. Dropping them changes nothing
  observable and costs about 900 names of test churn. No node needed.
- (2) Instance dicts: walking them is NOT the fix, because it is unbounded and still misses the registry shape. F2 closes
  the case that matters (rebinds). The write-reach residue becomes a docstring line (part of F2).

### Q5 -- standing items

- **Fit to the DoD**: there is no second compile (the row `install compiles nothing a second time` has a positive
  control), the facts come from live code objects, and the old rows are green. The equivalence table explains every
  difference, name by name: old-only = import-time-only, new-only = dataclass/NamedTuple generated code. The negative
  controls M0-M3 are reported red. The timing is consistent with t-079 F1: the `install` share 0.540 -> 0.007 s matches the
  `--help` drop 1.584 -> 0.987 s. My `import story_run` took 1.125 s in a process loaded with other imports. That is
  consistent, not a re-measurement.
- **DUPLICATION**: none in package code. I grepped `get_instructions|co_code|dis\.opmap` over `scripts/` and `tools/`. The
  only other hit is `tests/driver_golden.py:600`, a co_consts walk for another purpose. The test's `dis_scan`
  (test_module_facade.py, new) is the old `_scan` body kept as the oracle. With F1 it should become the module's
  `_scan_dis` (one copy, used by both the fallback and the test).
- **CODE QUALITY**: `_live_codes` 116-173 (58 lines, with the nested `visit` 127-169 at 43 lines and four branch levels) is
  at the limit, but acceptable for a type dispatch. Line 200 `codes, access, skipped[...] = _live_codes(mod)` binds the
  CLASS-MEMBER names to a variable called `access`, and the docstring calls them "names its classes bind". Rename it to
  `members` (F4, fix with the round). The module is 374 lines. F5 (note): `visit` does `getattr(obj, "__dict__")` (line 166)
  and `callable()` on ARBITRARY module-level objects, and the old code touched none of them. A proxy whose `__getattribute__`
  raises something other than AttributeError would abort `install`. It is not present in the parts. Optional: wrap it, and
  add the name to `skipped`.
- **ARCHITECTURE**: AR-15 is kept: one facade and one `_scan` (F1 adds a fallback inside the same function, not a second
  road). AR-12: start-up cost is down, which is the point. AR-14/AR-22: the `skipped` field has a producer and no reader
  except tests and debugging. That is acceptable, and it is documented as debug.
- **JUDGMENT**: none. The census unit with `raise ValueError` was not moved. The builder ran judgment_census 22/22.
- **ONE ROAD**: none found. The scan branch is per interpreter and gives the same output. F1's fallback serves the same
  condition, and the shared mechanism is still reached. There is no language/project exclusion (I grepped the diff for
  version and name branches: only `_GLOBAL_ARG_SHIFTED`).
- **Tests can fail**: yes. M2 turns `recorded set equals ...` and the scan-equals-dis rows red (reported). `global in a
  method ... refused` fails if the class-member walk is dropped. The callable-object row pins `skipped`. One gap: no row
  pins the shapes of Q4 (F2 adds it). One limit: `scan equals dis` proves only the Python the test runs on, which is 3.12
  on CI.
- **Class completeness** (SIBLING_MAP): the map has no facade/bytecode axis (I grepped `facade|module_facade|bytecode` in
  docs/SIBLING_MAP.md: 0 hits). The class "a code fact read from a source other than the full module code" lives only in
  this module.

## Fixes

- **F1 (fix in this round)** module_facade.py:87-111. Keep the `dis` reference as `_scan_dis` (the test's `dis_scan`
  body). On the first `_prepare` of a process, compare `_scan` with `_scan_dis` on a fixed probe:
  - the probe holds 300 names plus a function with `global`/`del` and a class body (LOAD_GLOBAL with and without
    EXTENDED_ARG, STORE/DELETE_GLOBAL, LOAD/STORE_NAME, and LOAD_FROM_DICT_OR_GLOBALS where it exists);
  - on a mismatch or any exception (IndexError), use `_scan_dis` for the rest of the process. Also catch IndexError per
    code object.
  - add a test row, "on this Python the fast scan is active". It goes red on CI the day CI's version breaks the fast path,
    so CI is loud while the field stays safe.

  Cost: about 3 ms per process.
- **F2 (fix in this round)** module_facade.py:194-208. For a part whose source text matches `(?m)^\s*global\s` (spec.origin
  read as bytes; a hit inside a string or comment only costs time), take `rebound` from `_scan` of the loader's module
  code for THAT part only. That is the old path, and it costs nothing for the 17 driver parts. Add a test row with the
  `instance_attr` shape that is refused. Docstring NOT COVERED: "a name read only by code that is reachable neither from
  the part's dict nor from its classes (an instance attribute, a foreign registry) is not reached by a write through the
  facade".
- F4 (with the round): line 200, rename `access` to `members`.
- F3 / F5: notes; no node is required.

## Not checked

- 3.10, 3.11, 3.13, 3.14: no interpreter here, so the analysis above is argued, not run.
- I did not re-run test_story_run_words, test_driver_chain, judgment_census or the timing; they are taken from the
  builder's verbatim layer, which is consistent with the diff.
- I did not re-run the M0-M3 mutants.
- The clone ratchet output was not attached.

## Trail

- Read: `git -C <wt> diff` of both files; module_facade.py 1-75, 200-374; report t-082; critic-diff-brief.md; verdict schema.
- Interpreters: `py -0p` -> only `-V:3.12 * ...Python312\python.exe`; `ls AppData/Local/Programs/Python` -> `Launcher Python312`.
- Control re-run: `python -B .../tests/test_module_facade.py` -> `=== test_module_facade: 124/124 ok ===`.
- Battery (stdin payload, read-only):
  - `[plain] mismatches=0 rebound_names=290 fast=0.31s dis=8.26s`
  - `modules with EXTENDED_ARG: 764`
  - `specialized: adaptive != co_code: True | fast==dis: True`
  - `instrumented+ran: ... fast==dis: True`
  - `[after set_local_events on 9702 codes] mismatches=0`
  - `probe(300 names): compile 1.05 ms, fast+dis 1.95 ms, equal=True`
- Real driver (`import story_run`):
  - `parts 17 skipped {}`, `live codes (top) 872`
  - `misread LOAD_GLOBAL arg: IndexError in 664 of 872`
  - `dis over 1339 code objects: 0.259s`, `live walk only: 0.0024s`, `rebind prefilter: 0 hits, 0.0020s`
- Q4 shapes: output quoted above.
- Greps:
  - production writes through story_run: 1 hit (a comment); control: 4 test files
  - `^\s*global\s`: driver 0, scripts 18
  - version floor: INSTALL.md:127 "Python 3.10+"; workflows pin "3.12"
  - `get_instructions|co_code|dis\.opmap`: driver_golden.py:600 only

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "No SIBLING_MAP axis covers the facade or bytecode scanning (grep facade|module_facade|bytecode in docs/SIBLING_MAP.md: 0). The class 'code facts read from live objects instead of the full module code' exists only in module_facade.py; its residue (rebinds in code not reachable from the part dict) is F2 in this round.",
  "trail": {
    "read": [
      "ai-packages/qa-factory/scripts/module_facade.py (worktree diff, lines 1-75, 200-374)",
      "ai-packages/qa-factory/scripts/tests/test_module_facade.py (worktree diff)",
      "docs/tasks/specs/reports/t-082-td11-facade-startup.md (worktree)",
      "docs/tasks/critic-diff-brief.md",
      "tools/critic_verdict.schema.json",
      "ai-packages/qa-factory/INSTALL.md:127 (floor 3.10+), .github/workflows/*.yml (python-version 3.12)"
    ],
    "reruns": [
      {"command": "python -B <wt>/ai-packages/qa-factory/scripts/tests/test_module_facade.py", "result": "=== test_module_facade: 124/124 ok ==="},
      {"command": "stdin battery: _scan vs dis over 2910 stdlib modules, plain and after sys.monitoring set_local_events on 9702 codes, specialized and instrumented functions", "result": "mismatches=0 (plain), mismatches=0 (instrumented), 764 modules with EXTENDED_ARG, 290 rebound names, fast==dis on specialized and instrumented-run code"},
      {"command": "import story_run; flip _GLOBAL_ARG_SHIFTED; scan 872 live codes", "result": "IndexError in 664 of 872 code objects: a misread version kills the driver at import"},
      {"command": "in-memory install of three part shapes (instance attribute, foreign registry, function attribute) with a global rebind and a second part binding the name", "result": "all three INSTALLED (refusal missed), skipped empty; stale mirror part.CACHE=2 facade.CACHE=0"},
      {"command": "py -0p", "result": "only -V:3.12 installed; 3.10/3.11/3.13/3.14 argued, not run"}
    ]
  },
  "fixes": [
    "F1 module_facade.py:87-111 -- keep a dis reference _scan_dis (the test's dis_scan moves here); once per process compare _scan with _scan_dis on a fixed probe (300 names, global/del, class body); on mismatch or any exception use _scan_dis for the process, also catch IndexError per code; test row: the fast scan is active on this Python",
    "F2 module_facade.py:194-208 -- for a part whose source matches (?m)^\\s*global\\s take rebound from the loader module code of that part only (old path; zero cost for the 17 driver parts); test row with the instance-attribute shape refused; NOT COVERED docstring line on writes not reaching code unreachable from the part dict",
    "F4 module_facade.py:200 -- rename the variable access that holds class-member names to members"
  ]
}
```
