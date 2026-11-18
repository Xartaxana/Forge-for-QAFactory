# t-1162: critic re-review of the S10 fix round (RD1-18, t-1155, commit 17394d5b over 45999d8a)

Verdict: **fit with fixes** (fit_with_fixes). No blocker. F1-F5 of t-1153 are fixed. The new logic (deviation 1) is sound:
no import cycle, refusal text byte-identical, shipped data at zero problems. Three small residuals are left (N1-N3). N1 is
the same class as F1. All three are one-line edits with no new logic, so the Lead can make them at merge without another
critic pass. That is a proposal: accepting the work is the Lead's decision (rule 6).

Scope: `git diff 45999d8a 17394d5b` in worktree agent-ad5f243604d67cfbd (9 files, +113/-54), judged against my verdict
t-1153 (F1-F6) and the two deviations the dispatch names.

## F1-F5 of t-1153

| F | status | evidence |
|---|---|---|
| F1 deny set = in-code list + run_forms launchers/shells + writers, renamed, about text, coupling, test rows | **fixed** (residual N1) | `hooklib._NEVER_READ_HEADS` (hooklib.py:1183-1191) is the in-code list plus the writers and aliases I asked for. `_load_run_forms` builds `never_read = _NEVER_READ_HEADS \| frozenset(launchers) \| frozenset(shells)` (:1321). `launchers` already includes `wrappers` (:1307-1308), and keys are lower-cased by the loader. Probe: never set has 73 words and includes timeout, uv, npx. The about text at launch-causes.json:101 names the run_forms tables, the writer list, and the `reader_runs` coupling for `fd -x` / `git -c`. The HEAD_TABLES row now holds timeout, uv, rm, Copy-Item, ICM, and is checked for BOTH table names |
| F2 one reader for launch-causes.json; skipped rows named | **fixed** | `_load_reader_heads` runs inside `_load_run_forms` (:1322) and appends a problem for each bad row: not a word, denied, or a table that is not a list. `head_rows` now lives in hooklib and reads `run_forms()["reader_heads"]`. stage_guard dropped its `host_adapter` import (stage_guard.py:77-80; the remaining `host_adapter` imports at :664/:673 are function-local, pre-existing). New test rows: test_run_forms k6 `bad_heads` (3 skipped rows give 3 named problems, and the valid rows stay) and k1 (shipped data: `run_forms_problems() == []`, which now covers reader_heads). The SIBLING_MAP:284 row still does not name `reader_heads`. The dispatch assigns that edit to the Lead at merge, so it is not a builder finding. It stays open until the merge commit |
| F3 duplicate test rows | **fixed** | test_stage_of_dispatch keeps only `READER_COMMANDS == floor`, and the `cases` loop is gone. `"python x.py"` is dropped from REFUSED_HEADS. The table is parameterised over both names in test_role_policy_reads (the `renamed`/`want2` lines). Traced: each HEAD_TABLES row either holds `role_read`, so `renamed` carries the same rows to `runner_mention`, or is a malformed shape, passed as-is, which gives the floor for both. `want2` = floor2 + the new words of `want`. For "bat" that gives floor2+("bat",), and every other row gives floor2. Re-run 233/233 |
| F4 `_is_reader` docstring and the path row | **fixed** | The docstring (stage_guard.py:2595-2598) says the caller strips the path. It also says why only `.exe` comes off, unlike `hooklib._name`. The `/usr/bin/rg` row is gone from the non-reader list. A junction pin `not _launches_runner("/usr/bin/rg " + mention)` records today's door |
| F5 (a) top import, (b) re.escape, (c) role_replay comment | **fixed** | (a) moot: `head_rows` moved to hooklib, and host_adapter imports it at the top (:14). (b) `read_head_regex` escapes each head (`Get\-Content` in the pattern; it still matches only the literal). (c) the comment names `HA.READ_HEADS` |
| F6 (process: FR pass) | not the builder's | still the Lead's item at acceptance (attach the FR pass or accept my t-1153 walk) |

## The two deviations

**Deviation 1 (the deny list and head_rows moved into hooklib; run_forms carries the parsed tables): accept.** It is the
preferred form of F2. The loader needs the run_forms launchers to build the deny set, so the parse has to sit next to them.
Checks:
- Import cycle: none. hooklib imports host_adapter only inside `read_event` (:936) and at :2732. `_load_run_forms` reaches
  neither. Probe, three fresh processes importing `host_adapter`, `stage_guard` or `hooklib` first, then both others: each
  prints `ok 7 27` (READ_HEADS 7, READER_COMMANDS 27).
- Load cost: host_adapter's import now runs `run_forms()` instead of `load_ref_json`. Probe: `load_ref_json` 0.35 ms,
  `run_forms` first load 1.80 ms, once per process (cached). stage_guard no longer pays the host_adapter import (about 13-15
  ms in t-1153). Net gain.
- Broken file: `_load_run_forms` catches the read error and sets raw = {}, so `reader_heads` comes back empty and both
  consumers keep their floor (FR-59 held). The deny set is computed before the fallback launchers join, but the fallback
  programs (python, python3, bash, sh, zsh, pwsh, powershell, cmd) are all in `_NEVER_READ_HEADS` already, so this costs
  nothing.
- `reader_heads(data)`: the probe path checks a caller's parsed data against the REAL file's deny set and drops problems.
  Only tests pass `data`. The production consumers call `head_rows(name, floor)`. Acceptable.
- Refusal text byte-identical. Probe: `_read_refusal("python x.py")` gives `it does not start with a read command (rg, cat,
  ls, pwd, Get-Content, Get-ChildItem, Select-String)`.

**Deviation 2 (cp and mv dropped from the shipped `runner_mention` rows; the stage_guard floor keeps them): accept as is.
Do not exempt the floor from the deny list.** Behaviour is unchanged. `READER_COMMANDS` has 27 entries and equals
`_READER_FLOOR` (probe, plus test_stage_of_dispatch `READER_COMMANDS == frozenset(SG._READER_FLOOR)`, green). An exemption
would need the loader to know each consumer's floor, which lives in the consumer. That puts consumer data into the shared
reader, or worse, a global exemption would let `cp` into `role_read` as well. That is the wrong direction for the read
guard. For the record: writers are harmful only to the `role_read` table. For the runner guard, only launchers and shells
matter (`cp run_suite.py x` launches nothing). So a per-table deny set (writers for `role_read` only) would keep the data
equal to the floor. The single deny set came from my own t-1153 F1 ("in both lists"). It is over-strict for
`runner_mention` but refuses only rows, never the floor, and the about text states the cp/mv case. I do not ask for the
per-table form.

## New findings (residuals of this round)

**N1 (minor, same class as F1, the read-guard deny list). The aliases of the cmdlets the round newly listed are missing,
which contradicts the list's own comment.** hooklib.py:1184-1186 says "file writers/deleters with the aliases of the
cmdlets listed". The round added Copy-Item, Move-Item, New-Item, Rename-Item and mkdir, but not their aliases: `cpi`,
`copy`, `mi`, `move`, `ni`, `rni`, `ren`, `md`. Probe (row patched into `role_read`, READ_HEADS and the regex rebuilt):
`copy secret.json out.json`, `cpi a b`, `ni evil.ps1` and `md newdir` each give `_read_refusal(...) == ''`, so the command
passes for a role without Bash. This only matters if someone adds a bad row to shipped, reviewed data, so it is minor. But
the comment claims a protection the list does not give. Fix: add `cpi, copy, mi, move, ni, rni, ren, md` to
`_NEVER_READ_HEADS`, plus one of them (e.g. `copy`) to the HEAD_TABLES writer row. Surface walk (rule 14): the same probe
also accepts make, curl, wget, ln, chmod, install, rsync, git and fd. git and fd are covered by the about text's
`reader_runs` coupling. The others are open-ended writers and runners outside what the comment claims, so they are not
required. I name them for the Lead's information only.

**N2 (minor, code quality). Stale docstring.** hooklib.py:1197-1198 (`_load_reader_heads`) says "The in-code floors of the
consumers stay outside, in `host_adapter.head_rows`". `head_rows` is now `hooklib.head_rows`, and the floors live in the
consumers (`host_adapter._READ_HEAD_FLOOR`, `stage_guard._READER_FLOOR`). Fix: "...stay with the consumers and are joined by
`head_rows`".

**N3 (minor, tests: a duplicate pin). The new k1 count row adds no behaviour.** test_run_forms.py:90-91 checks
`{role_read: 7, runner_mention: 25}`. "No row skipped" is already proved by the line above it (`run_forms_problems() ==
[]`; every skip now appends a problem). "None lost" has no behaviour behind it, because the floor makes a removed row
harmless. So the row only pins the table's size, and a legitimate new row would have to edit it. Fix: delete the row, or if
the Lead wants it kept, give it a reason in its label. Not blocking.

## Standing questions

- **Fit to the re-review DoD:** each F1-F5 judged (table above). Both deviations judged. The new logic is judged under
  deviation 1.
- **Class-wide completeness:** the deny class now reads the run_forms data (launchers, shells, wrappers). The residual is
  N1 (aliases). The table-family axis SIBLING_MAP:284 is a Lead edit at merge per the dispatch's `siblings:` line, still
  open in the diff.
- **DUPLICATION AND CONSISTENCY:** N3 (count pin duplicates `problems == []`) and N2 (comment ↔ code). The second loader
  of t-1153 F2 is gone. Grepped: `WRITER_HEADS|_HEAD_WORD|head_rows` over the package (`.py`, `.json`, `.md`). There is no
  leftover `WRITER_HEADS` anywhere; `head_rows` is defined only in hooklib.py:1232, and the other `head_rows` hits in
  test_manifest_from_tests/test_story_run_delivery are unrelated local variables. Also grepped
  `run_forms_problems|["problems"]` over the scripts: the only production reader is `hooklib.run_forms_problems`
  (:1357). Others are unrelated `problems` keys. So adding reader_heads problems to that list changes no other gate's
  meaning.
- **CODE QUALITY:** N2. `_load_reader_heads` is 25 lines with 3 nesting levels, fine. `reader_heads(data)` puts the probe
  path into production code, which was pre-existing in `head_rows`' signature. Acceptable.
- **Tests (q5):** killing power: the k6 `bad_heads` row fails if the deny `problems.append` is dropped (count 3). The
  HEAD_TABLES timeout/uv rows fail if `never_read` loses the launchers. The builder reports 32/32 k19 mutants killed, which
  I did not re-run. Volume of the round: tests +28/-15, product +85/-39, so tests are under product and no `tests-over:`
  line is owed. No new test file.
- **ONE ROAD (q12):** improved. The guard's tables in launch-causes.json now have one reader (`hooklib.run_forms`). No
  language, project or case is excluded.
- **ARCHITECTURE:** the commit names AR-1 and AR-13/AR-15, and both are kept as stated (data rows with an in-code floor;
  one reader). **JUDGMENT:** `judgment: none` holds, and the census re-run is 25/25.
- **Hygiene:** 0 CR, 0 Cyrillic, 0 control bytes in the diff. The changelog fragment is English and names `hooklib.head_rows`.
- **Commit message** carries `architecture:`, `judgment:`, `axes: not a mechanism (...)`.

## Trail

Read: my verdict docs/tasks/specs/reviews/t-1153-rd1-18-s10-code.md; `git diff 45999d8a 17394d5b` (full); the commit
message of 17394d5b; hooklib.py :925-945, :1060-1100, :1178-1245, :1268-1360; host_adapter.py :11-15, :453-470, :542-567;
stage_guard.py :77-80, :660-675, :2505-2520, :2593-2600; test_role_policy_reads.py :240-290; launch-causes.json :1-100
(wrappers, launchers, shells), :101; docs/SIBLING_MAP.md :280-288 (worktree).

Re-runs (worktree package dir, HEAD 17394d5b, clean tree):
- `python -B scripts/tests/test_role_policy_reads.py` gives `=== test_role_policy_reads: 233/233 ok ===`
- `python -B scripts/tests/test_run_forms.py` gives `=== test_run_forms: 309/309 ok ===`
- `python -B scripts/tests/test_stage_of_dispatch.py` gives `=== test_stage_of_dispatch: 20/20 ok ===`
- `python -B scripts/tests/test_judgment_census.py` gives `=== judgment_census: 25/25 ok ===`

Probes (scratchpad `probe_s10b.py`, `probe_s10c.py`, worktree code, no repo file touched):
- import order host_adapter / stage_guard / hooklib first: `ok 7 27` each
- refusal text identical; pattern `(?:rg|cat|ls|pwd|Get\-Content|Get\-ChildItem|Select\-String)(?:\s|$)`; problems `[]`
- never set 73 words; timeout/uv/npx in, make not in
- `role_read +=` cpi/copy/mi/move/ni/rni/ren/md: each accepted; `_read_refusal('copy secret.json out.json') -> ''` (N1)
- `load_ref_json 0.35 ms; run_forms first load 1.80 ms`

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "F1 deny class now reads run_forms launchers, shells and wrappers plus an in-code writer list; residual N1: the aliases of the newly listed cmdlets (cpi, copy, mi, move, ni, rni, ren, md) are missing although the list's comment claims them. F2 one reader for launch-causes.json reached (hooklib.run_forms). Table-family axis SIBLING_MAP:284 still does not name reader_heads: a Lead edit at merge per the dispatch, open.",
  "fixes": [
    "N1 hooklib.py:1183-1191 _NEVER_READ_HEADS: add cpi, copy, mi, move, ni, rni, ren, md (aliases of Copy-Item, Move-Item, New-Item, Rename-Item, mkdir, which the comment says are covered); add 'copy' to the HEAD_TABLES writer row in test_role_policy_reads.py",
    "N2 hooklib.py:1197-1198 _load_reader_heads docstring: head_rows is hooklib.head_rows now; the floors stay with the consumers",
    "N3 test_run_forms.py:90-91 the k1 count pin {role_read: 7, runner_mention: 25} duplicates run_forms_problems() == [] and pins table size only: delete it or give it a reason",
    "Lead at merge: SIBLING_MAP.md:284 names reader_heads and its reader hooklib.head_rows/run_forms; F6 FR pass attached or the t-1153 walk accepted"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/reviews/t-1153-rd1-18-s10-code.md",
      "git diff 45999d8a 17394d5b (worktree agent-ad5f243604d67cfbd) and commit message",
      "ai-packages/qa-factory/scripts/hooklib.py:925-945,1060-1100,1178-1245,1268-1360",
      "ai-packages/qa-factory/scripts/host_adapter.py:11-15,453-470,542-567",
      "ai-packages/qa-factory/scripts/stage_guard.py:77-80,660-675,2505-2520,2593-2600",
      "ai-packages/qa-factory/scripts/tests/test_role_policy_reads.py:240-290",
      "ai-packages/qa-factory/references/launch-causes.json:1-101",
      "docs/SIBLING_MAP.md:280-288"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_role_policy_reads.py (worktree package dir)", "result": "=== test_role_policy_reads: 233/233 ok ==="},
      {"command": "python -B scripts/tests/test_run_forms.py (worktree package dir)", "result": "=== test_run_forms: 309/309 ok ==="},
      {"command": "python -B scripts/tests/test_stage_of_dispatch.py (worktree package dir)", "result": "=== test_stage_of_dispatch: 20/20 ok ==="},
      {"command": "python -B scripts/tests/test_judgment_census.py (worktree package dir)", "result": "=== judgment_census: 25/25 ok ==="},
      {"command": "python -B probe_s10b.py <worktree scripts> (scratchpad)", "result": "import order: ok 7 27 x3; refusal identical; problems []; never 73 words with timeout/uv/npx; role_read += cpi/copy/mi/move/ni/rni/ren/md accepted"},
      {"command": "python -B probe_s10c.py <worktree scripts> (scratchpad)", "result": "load_ref_json 0.35 ms; run_forms 1.80 ms; _read_refusal('copy secret.json out.json') -> '' with row copy"}
    ]
  }
}
```
