# Spec facts by code, spec judgment by the plan critic (t-897, F19) — DRAFT, fix round 1 (t-913)

Designer draft from the Lead's intent brief (t-897), revised after the plan critic t-904 (verdict: go with fixes; B1-B6,
M1-M11). Forks are returned (section F); forks the Lead or the owner already decided are marked so there, with the
carrier. Status: fix round 1 done, awaiting Lead acceptance. A second critic pass is owed only if the Lead finds these
fixes change the architecture (PROJECT.md «новая идея», step 6); the new forks F-11..F-13 are listed for the Lead.

Evidence the brief rests on: scout t-896 (accepted), carrier `logs/journal/dev1.jsonl`, 65 lines with
`"failure_class":"spec"` 11-16.11.2026 (the critic re-counted 65: review t-904 trail). The scout's per-line class list
(the "30 code-fact rejects") has NO persisted carrier (review B6, journal 2196) — §6 step M-1 creates one.

---

## §0 The Lead's reading, checked against the evidence

The Lead's reading: classes a, e, c are DATA about the repo (belong to code, P27); b, d are judgment (belong to a
critic rule). What the re-read lines show:

- **Class a splits in two.** (a1) *who else reads, pins or quarantines the changed thing* — data a search can
  answer. (a2) *what the existing code actually does* — line 417 ("value() has no element arg"), 551 ("my spec
  assumed an install signature in the receipt; it has none"), 1972 ("--part exits:<group> does not exist"), 829's
  cause ("Spec missed selftest's no-hooklib rule (:93)"). No reader list shows a missing argument, a field that is not
  there, or a rule inside the changed file. a2 is closed by a PREMISE (command + output, file:line + quote) the plan
  critic spot-runs — PART 2 (c). Partial help for a2 from code: name presence on the base (§2.3 (v)).
- **Class c is not data the tool can see** (journal 2172, t-885: the Linux exec bit). PART 1 does not claim it.
- **Class e** is data when "a test outside owns pins the old state" (names hits, §2.3 (v)) and when "the node rests
  on an unmerged branch" (presence, §2.3 (iv) for paths, (v) for names — line 541 is a FUNCTION on an unmerged branch).
- **b and d are judgment** — agreed; PART 2 (a)/(b).

**What is proven and what is not (review B6).** The replay (§R, corrected) gives PART 1 firm catches only in two
sub-classes: a test file in quarantine named by the dispatch (lines 384, 397, 1060, 1115) and a name absent on the base
(541, through `--names`). Lines 1395 and 1117 are caught only by name-level hits, and only if the dispatcher passes the
right name. **The literal file-name reader list has ZERO firm catches among the replayed rows; its yield on the 30
code-fact rejects is UNPROVEN** — the 30 have no carrier and nobody has replayed the tool on their dispatches. So this
spec ships the reader list as COUNTS by default and makes the listing a measured phase 2 (§6 M-2, rule 10 (d):
promotion follows evidence).

**Is the cheapest version enough?** Review item 8 names it: layer status (ii) + presence (iv) + `--names` presence and
hits (v), with the literal reader list behind a count — it catches every firm replay hit (384, 397, 1060, 1115, 541)
plus 1395 and 1117 when the name is passed. That is phase 1 below; the listed reader form waits for M-2's numbers
(the exact phase boundary is fork F-12).

So the direction holds with one correction: PART 2 carries a third duty besides edges and meaning — the PREMISE for
every statement about existing code — because a2 is the share of class a that PART 1 cannot reach.

---

## §1 What changes, and the owner each check serves

| # | Change | Owner served (P27) | Census class |
|---|---|---|---|
| C1 | New forge tool `tools/owns_readers.py`: for owned/given paths and named names it prints layer status of test files (quarantine, slow), presence on the base, name hits and name presence, reader COUNTS (listing on `--readers`) | **data (code)** — it gathers facts, decides nothing; it never says "the spec is complete"; its header carries counts and the search method, no verdict word (M2) | n/a — a forge tool; `judgment-census.json` covers `ai-packages/` only |
| C2 | `tools/dispatch_new.py` builds the tool's block, checks headers + block through the launch hook's own decision, prints both | data (code) | n/a (forge) |
| C3 | `tools/dispatch_manifest.py` adds a NOTE (never a refusal) when a writing dispatch carries no `readers:` line | data (code): presence of a line only | n/a (forge) |
| C4 | Plan-gate question for the critic (edges, meaning, premises, readers) | **judgment (a role — the critic), accepted by the Lead** | n/a (role text) |
| C5 | One line in `.claude/agents/designer.md` rule 3: the readers list comes from C1's output | judgment (designer), accepted by the Lead | n/a |
| C6 | A convergence node (L9): one answer to "which tests concern this package path" (`scenario_walk.py --witness-for` vs C1) | data (code), node owner: the Lead of pile `forge` | n/a (a queued node) |

**AR-n**: this spec changes no file under `ai-packages/qa-factory/` — `architecture: none -- forge tools and role
texts only` (fork F-11 keeps it so). It READS two package files at the base revision:
- `scripts/tests/test-layers.json` — through the forge's existing revision reader
  `tools/test_quarantine.py::_blob_sections(root, rev)` (premise P6), in ONE isolated function (§2.3 (ii)-q);
- `scripts/slow_tests.json` — through the package's ONE reader's validator `selftest._slow_tests_problem(raw)` and the
  reader's own meaning, MEMBERSHIP in `files` (premise P7, corrected; review B5). No threshold is applied.
The spirit of AR-13 (a fact with a reader function is read only through it) is kept for both: no second parser.

---

## §2 The tool `tools/owns_readers.py`

### 2.1 Inputs

```
python -B tools/owns_readers.py --paths <p>... [--given <p>...] [--names <n>...] [--base <ref>] [--repo <dir>] [--readers] [--all]
```

- `--paths`: owned paths (absolute or repo-relative; a trailing ` (new)` marks a new file, the marker `dispatch_new.py`
  uses, premise P1). At least one; empty → exit 2 with a door (E-1).
- `--given`: given paths — checked for presence and layer status only; readers are not counted for them.
- `--names`: names the spec changes or introduces (functions, keys, flags, constants); a trailing ` (new)` marks a
  name the dispatch asks the builder to CREATE (review B2). At most 20 (`names_cap`, S-2); beyond → one `unsearched`
  line naming the count.
- `--base`: the tree searched; default `origin/main` (F-1, decided). Any ref works, so a historical replay passes the
  commit before a reject's fix (§6 M-2). `--repo`: the repo root; default the parent of `tools/`.
- `--readers`: render the reader LIST (tests first, §2.4 caps) instead of the per-path count line. Phase 1:
  on demand and for M-2; phase 2 (if M-2 promotes it): what `dispatch_new` prints.
- `--all`: lift every listing cap and list code readers and quarantined readers too (implies `--readers`).

Python API (what `dispatch_new.py` calls): `report(paths, given=(), names=(), base="origin/main", repo=None) ->
Report` and `render(report, readers=False, all_=False) -> str`. Writes nothing. Git reads go through `tools/gitcmd.git`
(premise P8), EXCEPT the `git show` inside the reused `_blob_sections`, which runs `test_quarantine._git` (its own
runner, timeout 120, any exception → rc 128; premise P6) — named here and in the docstring (review M4).

### 2.2 Output — exact shape

One header line `readers: ...`, then at most the lines §2.4 allows, each starting `- <kind>:`. Every path printed is
REPO-RELATIVE with forward slashes; a path outside the repo is printed by its base name only (§3.1 invariant, M3).

**Header forms** (neutral words: counts and the method, no verdict — M2):

```
readers: <R> outside owns, <L> lines below -- base <ref> <sha8> (literal mention; known misses: tools/owns_readers.py docstring)[; quarantine: unknown (<why>)][; slow: unknown (<why>)][; presence: unknown (<why>)][; names: unknown (<why>)]
readers: unknown -- git grep exited <rc> (<first stderr line>); <L> lines below -- base <ref> <sha8> (...)[; ...]
readers: unknown -- base <ref> does not resolve here (git: <first line>); nothing was searched
```

`<R>` = readers outside owns of all owned paths, deduplicated by file (a quarantined reader counts). `<L>` = the
number of `- ` lines. `<sha8>` = the base commit actually searched. An `unknown` segment is printed for every fact
that could not be established; it is never omitted and never rendered as zero (FR-59).

**Kinds, in this order** (the firm-catch facts first, review B1):

| kind | when | text |
|---|---|---|
| `hot` | an owned path has more than `test_cap` (25) non-quarantined test readers AND no `--names` was given | `- hot: <path> -- <N> test readers; pass --names <the functions or keys you change> for a usable list` |
| `quarantined` | an OWNED or GIVEN test file is in the `quarantine` section at the base | `- quarantined: <path> (owned\|given) -- the canon does not run it; a case goes to a keep file` |
| `slow` | an OWNED or GIVEN test file is listed in `slow_tests.json` `files` at the base | `- slow: <path> (owned\|given) -- listed slow: not run locally, judged by the batch canon` |
| `absent` | a given or owned (not new) path is not on the base; a non-new name has zero hits in the whole base tree | `- absent: <path> (given\|owned) -- not on <ref> <sha8>; a worktree builder cannot read it` / `- absent: name <n> -- not named anywhere on <ref> <sha8>` |
| `exists` | an owned `(new)` path is on the base; a `(new)` name already has hits | `- exists: <path> (new) -- already on <ref> <sha8>` / `- exists: name <n> (new) -- already named by <K> files on <sha8>` |
| `names` | a name has a hit in a scope file outside owns | `- names: <reader> (test\|test, slow\|data) names <n>` (code and quarantined readers of a name go into its `more` line) |
| `outside` | `--readers` only: a test reader of an owned path | `- outside: <reader> (test\|test, slow) names <owned file>[, <owned file 2>]` |
| `data` | `--readers` only: a data carrier naming an owned path | `- data: <carrier> names <owned file>` |
| `more` | one line per subject (owned path or name) with anything counted and not listed | `- more: <path>\|name <n> -- <T> test, <Q> quarantined, <C> code, <D> data readers not listed (--readers / --all lists them)` (zero parts omitted) |
| `unsearched` | a path outside the repo, a directory over 40 files, more than PATH_CAP paths, more than 20 names | `- unsearched: <base name> (outside the repo; pass the repo path)` / `- unsearched: <dir> holds <N> files; readers not counted -- name the files` / `- unsearched: <N> more paths\|names over the cap` |

Within `names`, `outside`, `data`: test readers first, ordered (S-7): namesake tests (file name starts with
`test_<stem>`), then files naming the full file name, then stem-only hits; alphabetical within each tier.

**Example A — default, nothing beyond counts** (S2's own owns, the critic's hand count, review item 2):

```
readers: 20 outside owns, 1 lines below -- base origin/main 0d6f61b1 (literal mention; known misses: tools/owns_readers.py docstring)
- more: tools/dispatch_manifest.py -- 9 test, 10 code, 1 data readers not listed (--readers / --all lists them)
```

**Example B — default, firm-catch facts**:

```
readers: 253 outside owns, 4 lines below -- base origin/main 0d6f61b1 (literal mention; known misses: tools/owns_readers.py docstring)
- quarantined: ai-packages/qa-factory/scripts/tests/test_import_test_receipt.py (owned) -- the canon does not run it; a case goes to a keep file
- absent: name require_project_at -- not named anywhere on origin/main 0d6f61b1
- names: ai-packages/qa-factory/scripts/tests/test_conductor_doors.py (test) names s0_criteria
- more: ai-packages/qa-factory/scripts/story_run.py -- 92 test, 81 quarantined, 68 code, 12 data readers not listed (--readers / --all lists them)
```

**Example C — the base cannot be read**:

```
readers: unknown -- base origin/main does not resolve here (git: <first line>); nothing was searched
```

**Example D — the search failed after the base resolved** (the rest of the block is kept, review B3):

```
readers: unknown -- git grep exited 128 (fatal: <first line>); 1 lines below -- base origin/main 0d6f61b1 (literal mention; known misses: tools/owns_readers.py docstring); quarantine: unknown (test-layers.json present at 0d6f61b1 but read empty)
- absent: docs/tasks/specs/x-spec.md (given) -- not on origin/main 0d6f61b1; a worktree builder cannot read it
```

### 2.3 How each fact is computed

All searches run on the BASE TREE through `git grep <sha>`, never the working tree (F-1). Reason, measured: the working
tree of this clone holds full repo copies under `.claude/worktrees/` (premise P9) and other sessions' uncommitted state.

**rc map for every git call (review B3).** `git grep`: rc 0 = hits, rc 1 = no hits, any other rc (128, and -1 which
`gitcmd.git` returns on a timeout or a start failure, premise P8) = UNKNOWN. `git ls-tree`, `git rev-parse`,
`git show`: rc 0 = read, anything else = UNKNOWN. An unknown becomes the header segment of its fact; it is NEVER
rendered as "0 readers", "not quarantined", "not slow", "present" or "absent".

**Base first.** `git rev-parse --verify --quiet <ref>^{commit}` resolves `<sha>`. Not resolved → Example C, nothing
else is run (every later fact needs the base).

**Search scope** (data, kept in `tools/owns_readers.json`, S-2). EVERY scope row is a pathspec with glob magic
`:(glob)<pattern>`, every excluded row `:(exclude,glob)<pattern>` (review M1: in git's default pathspec `*` crosses
`/` — `.../fixtures/*.json` matched 584 files by default against 13 with `:(glob)`, review trail). `git ls-tree` refuses
glob magic, so the tool's `ls-tree` calls take LITERAL paths only (owned/given paths, the two registry paths, a
directory in owns).
- tests: `ai-packages/qa-factory/scripts/tests/**/test_*.py`, `tools/test_*.py`, `tools/tests/**/test_*.py`;
- data: `tools/*.json`, `ai-packages/qa-factory/references/*.json`, `ai-packages/qa-factory/scripts/*.json`,
  `ai-packages/qa-factory/scripts/tests/*.json`, `ai-packages/qa-factory/scripts/tests/fixtures/*.json` (top level —
  true only under `:(glob)`), `ai-packages/qa-factory/design/*.json`, `ai-packages/qa-factory/scripts/audit_factory.py`
  (the py-tuple ratchets of critic-diff-brief item 9);
- code: `tools/**/*.py` (non-test), `ai-packages/qa-factory/scripts/**/*.py` (non-test), `.githooks/*`,
  `.claude/settings*.json`, `.claude/hooks/**`, `.claude/agents/*.md`, `.claude/skills/**/SKILL.md`;
- excluded: `ai-packages/qa-factory/scripts/tests/fixtures/stories/**`, `**/fixtures/run-*/**`.
A file matching two rows takes the first of tests, data, code. Known misclassification: `tools/test_quarantine.py` and
`tools/test_split.py` are TOOLS named `test_*` (premise P10) — counted as "test". Error direction: over-report, never a
reader dropped; this recognizer is a forge reader of "is this a test" with its own question (SIBLING_MAP axis 9,
the `tools/test_volume.py` precedent; L8).

**(i) Readers (counted; listed with `--readers`).** Patterns per owned path: its file name (`dispatch_manifest.py`) as
a fixed string, and its STEM as a whole word (`-w`) when the stem has 4 or more characters. One call:
`git grep -I -o -w -F -e <pat1> -e <pat2> ... <sha> -- <scope pathspecs>` (the same call carries the `--names`
patterns, (v)). Each hit is attributed to the owned path whose pattern it matched; a hit inside the owned file itself is
dropped; a hit inside another owned file is "inside owns" (not counted); every other file is a reader outside owns,
classed test / data / code by its scope row, a test further marked quarantined (from (ii)-q) and slow (from (ii)-s).

KNOWN MISSES, written into the tool's docstring (the plan critic's duty starts there, §4.1 (d)):
1. transitive readers (a test imports `a`, which imports the owned `b`) — for a package path
   `scenario_walk.py --witness-for` is the transitive list (premise P11);
2. a path built from pieces, a name read from data, `importlib` with a computed string;
3. a pin on a VALUE without the file name (line 1117: a frozen dict pinning `qa-retro-analyst 14075`) — `--names` only;
4. stems under 4 characters (searched by file name only);
5. readers outside the scope (docs, plans — prose readers are the designer's own walk);
6. a stale base: the tool does not fetch; the header prints the sha it searched;
7. a common-word stem of 4+ characters over-counts (measured: `contract` is a whole word in 537 scope files against 96
   naming `contract.py`, review item 2) — counts, never drops; in a listing it sinks to the third tier (S-7).

**(ii) Layer status of test files.** For every owned or given path under `ai-packages/qa-factory/scripts/tests/`, and
for every reader there. Forge tests (`tools/`) have no layer registry: no status is printed for them (the data row
does not exist — a real difference of data, not a branch on a name; P31), and the docstring says so.

- **(ii)-q quarantine — ONE isolated function** `_quarantine_status(repo, sha, present) -> (set_of_names | None, why)`,
  the tool's only import of `test_quarantine._blob_sections`. Registry presence comes from the tool's own `ls-tree`
  of (iv) (literal path `ai-packages/qa-factory/scripts/tests/test-layers.json`):
  - absent at the base → `None`, `quarantine: unknown (test-layers.json absent at <sha8>)`;
  - present, `_blob_sections` returns `keep` AND `quarantine` both empty (its answer on ANY `git show` failure,
    premise P6) → `None`, `quarantine: unknown (test-layers.json present at <sha8> but read empty)`;
  - present, `_blob_sections` raises `test_quarantine.Unknown` (malformed JSON, premise P6) → `None`,
    `quarantine: unknown (test-layers.json at <sha8> is not JSON)`; the rest of the block is kept (the exception
    never climbs to `dispatch_new`);
  - present, `keep` non-empty → the set of `quarantine` keys (an empty set is a real "nothing quarantined" — the
    world after the quarantine section is deleted).
  On `None`, no `quarantined` line is printed and no reader is counted as non-quarantined: the `more` lines print
  quarantined parts as `? quarantined` and the header segment says why.
  **Removal (the owner's open question of 17.11.2026 «может будет проще удалить все тесты что сейчас в карантине»):**
  `_quarantine_status`, its call, the `quarantined` kind, the `Q quarantined` part of `more` and the T1 row group
  `quarantine-*` are deleted TOGETHER with the quarantine section when the owner decides the deletion (L10 puts this
  line on the deletion's carrier). Until then the function is correct in both worlds: with the section present it
  reports, with the section gone (keep present) it is quiet — a forgotten deletion is dead code, never a wrong fact.
- **(ii)-s slow** — `_slow_status(repo, sha, present) -> (set_of_names | None, why)`: `git show
  <sha>:ai-packages/qa-factory/scripts/slow_tests.json` through `gitcmd.git`, `json.loads` of the text (utf-8-sig),
  then `selftest._slow_tests_problem(raw)` — the shape validator of the ONE reader `selftest.slow_tests`
  (premise P7). The selftest module is loaded from the TOOL'S OWN checkout (`_TOOLS_DIR.parent`), by
  `test_quarantine._pkg_module(root, "selftest")` (fork F-13). Slow = MEMBERSHIP: the file name is a key of `files`
  (the reader's meaning: `--fast` skips the files the list names, selftest.py:868, 1003-1005); no threshold. Absent,
  `git show` rc ≠ 0, not JSON, a problem phrase, or the selftest module failing to load → `None`,
  `slow: unknown (<why>)`.

**(iii) Data carriers.** A data-row hit of (i) is a data reader. This covers registries keyed by file name
(`tools/source-split-carriers.json` `carriers`, premise P12), the ratchets of critic-diff-brief item 9 in JSON or
`audit_factory.py`, `references/role-load.json` (keyed by role name = the role file's stem, premise P13),
`tools/install_parity_anchors.json`, `tools/warn_layers.json`. No carrier list is kept (F-3, decided).

**(iv) Presence on the base.** One `git ls-tree -r --name-only <sha> -- <literal paths>` call over owned, given and the
two registry paths. Owned (not new) or given absent → `absent`; owned `(new)` present → `exists`; owned `(new)` absent →
nothing. ls-tree rc ≠ 0 → `presence: unknown (<why>)`, no `absent`/`exists` line, and both registries are unknown.

**(v) Names (review B2, F-4).** Each `--names` item is a pattern in the (i) call: as a fixed string with `-w` when it
starts and ends with a word character, as a plain fixed string otherwise (`--part`, `exits:` — `-w` misreads them,
S-8). Its scope hits outside owns print as `names` lines (tests listed, then data; code and quarantined counted in the
name's `more` line), under the caps of §2.4. Presence: a second call over the WHOLE base tree (no pathspec) —
`git grep -I -o -h -F [-w] -e <n1> -e <n2> ... <sha>` — the set of matched strings is the set of present names.
A non-new name with zero hits → `absent: name`; a `(new)` name with hits → `exists: name`; a `(new)` name with zero
hits → nothing (expected: the temporal edge, the name exists only after the change). The presence call failing →
`names: unknown (<why>)`, no `absent`/`exists` line for any name.

### 2.4 Limits and worst-case block size

| Cap | Value | Applies to | Overflow |
|---|---|---|---|
| `test_cap` | 25 | test lines per subject (an owned path under `--readers`, or a name) | counted in the subject's `more` line; an owned path over it is `hot` |
| `data_cap` | 12 | data lines per subject | counted in `more` |
| code readers | count only | every subject | `--all` lists them as `- outside: <file> (code) names <x>` |
| quarantined readers (not owned/given) | count only | every subject | `--all` lists them with `(quarantined: the canon does not run it; do not edit)` |
| directory in owns | 40 tracked files at the base | `ls-tree` expansion | one `unsearched` line |
| paths | `dispatch_manifest.PATH_CAP` (200, premise P2) | owned + given | one `unsearched` line |
| names | 20 | `--names` | one `unsearched` line |

A hot path under `--readers` WITH `--names` given lists no test readers of its own (they go to `more`): the names lines
are the usable list (review B1's "instead of listing"). Invariant: a capped list is never presented as complete —
every overflow is counted in a `more` or `unsearched` line.

**Worst-case block sizes**, from the critic's counts (review item 2, M10; origin/main 0d6f61b1):

| Owned | Counts | Default block (phase 1) | `--readers` block |
|---|---|---|---|
| `tools/dispatch_manifest.py` + `tools/test_dispatch_manifest.py` | 20 outside: 9 test, 10 code, 1 data, 0 quarantined | 2 lines (header + one `more`); 3 if the owned test file has outside readers | 12 lines: header + 9 `outside` + 1 `data` + 1 `more` (10 code) |
| `ai-packages/qa-factory/scripts/story_run.py` | 253 outside: 173 test of which 81 quarantined (92 others), 68 code, 12 data | 3 lines: header + `hot` + `more` | 40 lines: header + `hot` + 25 `outside` + 12 `data` + 1 `more` (67 test, 81 quarantined, 68 code) |
| each `--names` item | — | at most 38 lines: 25 test + 12 data + 1 `more` (typical: a few) | same |

The old cost claim "1-15 lines per dispatch" is withdrawn. Time: ~0.2 s per grep, measured by the critic on both files
(review item 2), so a run is well under 5 s; wall time is never asserted in a test (FR-31). A git call over `gitcmd`'s
timeout → rc -1 → the unknown form of its fact.

### 2.5 Edge behaviour, each with its invariant

| E | Input | Behaviour | Invariant it protects |
|---|---|---|---|
| E-1 | `--paths` empty or all items blank | exit 2, stderr `OWNS_READERS REFUSED: no path given -- pass --paths <owned path>...` | the tool never prints a header about nothing |
| E-2 | base does not resolve / git missing / rev-parse timeout | exit 0, Example C only | an unknown never reads as "no readers" or "not quarantined" (FR-59); `_blob_sections` is never called on an unresolved base |
| E-3 | `test-layers.json` absent at the base | header `quarantine: unknown (... absent ...)` | absence of the registry is never read as "not quarantined" |
| E-3b | `test-layers.json` present, `git show` fails after the base resolved | header `quarantine: unknown (... read empty)` | a failed read is never "not quarantined" (review B3.2) |
| E-3c | `test-layers.json` malformed | header `quarantine: unknown (... not JSON)`; the rest of the block printed | one bad registry never wipes the other facts (review B3.3) |
| E-3d | quarantine section deleted, keep present | no quarantine line, no unknown | the post-deletion world is quiet, not unknown |
| E-4 | path outside the repo root | `- unsearched: <base name> (outside the repo; pass the repo path)` | a path the tool cannot search is named, and no absolute path enters the block (M3) |
| E-5 | owned `(new)` path / `(new)` name | §2.3 (iv)/(v): absent → nothing; present → `exists` | a "new" thing already on the base is named; a name the change introduces is never `absent` (review B2) |
| E-6 | directory in owns | §2.4 | a wide directory is named, never silently skipped |
| E-7 | no reader, no fact | header `readers: 0 outside owns, 0 lines below -- ...` | quiet on nothing to report (the owner's word 16.11, FG7-49); the method words say what "0" was measured by |
| E-8 | a path with spaces or Cyrillic | fixed string; printed as git holds it (`core.quotepath=false`, premise P8) | the printed path is the path git holds |
| E-9 | a file name or name starting with `-` | every pattern after `-e`, every path after `--` | a CLI argument never becomes a git option |
| E-10 | a short stem (< 4 chars) / a common-word stem (≥ 4, `config`, `contract`) | short: file name only (S-3); common: counted, sorted last in listings (S-7), KNOWN MISS 7 | noise inflates a count, never hides a capped line's overflow |
| E-11 | binary files in scope | `-I` skips them | — |
| E-12 | the same reader names two owned paths | one line, names joined; counted once in `<R>` | one line per reader file |
| E-13 | `--base` is another branch, a historical sha, or the run is in a detached worktree | searched as given (refs are shared by worktrees), header names ref and sha | the header always says what was searched |
| E-14 | `slow_tests.json` absent, unreadable, malformed, or the selftest module fails to load | header `slow: unknown (<why>)` | as E-3 |
| E-15 | `git grep` rc ∉ {0, 1} (128, -1) | header `readers: unknown -- git grep exited <rc> ...`; presence, layer and name-presence lines still printed | a failed grep never renders as `0 outside owns` (review B3.1) |
| E-16 | `ls-tree` rc ≠ 0 | `presence: unknown`; no `absent`/`exists`; registries unknown | a failed listing is never "all present" or "all absent" |
| E-17 | names over 20 / a name without word characters at its ends | `unsearched` line / matched without `-w` (S-8) | a name is never silently dropped or misread |

**Error direction (rule 1, a function reused in a more consequential role).** C1 is advice that feeds a NOTE and a
critic duty, not a gate. It may err toward OVER-reporting (a tool counted as a test, a comment mentioning a stem); it
must not err toward UNDER-reporting a literal mention in scope, a quarantined owned file, or an absent path or name —
and with caps, an over-reporting search would push real readers out of a listing, which is why every listing is
ordered (S-7) and every overflow counted. The reused `_blob_sections` errs toward "empty sections" on a git error and
raises on malformed JSON — both unsafe for this role, hence (ii)-q's presence-first rule. Adversarial inputs that must
stay on the safe side: E-2, E-3, E-3b, E-3c, E-14, E-15, E-16; a reader only in an untracked worktree copy (not counted
— correct, not on the base); a quarantined reader (counted with its status, never dropped); a capped list (overflow
counted); a `(new)` name (never `absent`).

### 2.6 What the tool never does

Fetches, writes, judges sufficiency ("this spec is complete"), refuses a dispatch, prints a verdict word in its header
(`ok`, `to act on`), or calls its index a "radius" (P27).

### 2.7 Its relation to `scenario_walk.py --witness-for` (review M9)

Two questions, two answers, stated in the tool's docstring and in `plans/builder-rules.md` 7b (L5): `--witness-for`
answers **what to RUN** for a package path (keep `covers` + import closure; the DoD names it, premise P11);
`owns_readers` answers **what must not break or be edited** (literal readers, layer status, presence). A convergence of
the two into one "who judges this path" reader is node C6 (L9), with an owner — not a residual line. Whether the split
is also stated in `scenario_walk.py` (a package file) is fork F-11.

---

## §3 Wiring

### 3.1 `dispatch_new.py`

New order in `main` (review B4):
1. The argument checks and `build_text(args)` as today → `headers`.
2. When the dispatch has owned paths: `block = owns_readers.render(owns_readers.report(owns, given, names))`; the tool
   raising anything → `block = "readers: unknown -- <ExcType>: <first line>\n"`. No owned paths (critic, designer,
   scout) → no block.
3. `text = headers + "\n" + block` (headers alone when there is no block). `_ids_refusal(args, text)` and
   `dispatch_gate.decide_full` run on `text` — the launch hook checks exactly what is printed, so C3's note never
   fires on the generator's own output, and the hook is a live check of the position invariant below.
4. `decide_full` refuses `text` → run it once more on `headers + "\n" + "readers: unknown -- the manifest check refused
   the block (<first line of its message>)\n"`. That passes → print it, exit 0, and one stderr line
   `OWNS_READERS: the manifest check refused the readers block -- a defect of tools/owns_readers.py; the block was
   replaced`. That refuses too → the refusal is the headers' own: today's behaviour (message on stderr, nothing on
   stdout, exit 2). Invariant: a failing helper never blocks or hides a dispatch, and never prints a count it did not
   measure; a refused dispatch still prints nothing on stdout (`test_dispatch_new.py:84-85`, premise P3).
- New optional `--names <n>...` passthrough (F-2, decided), ` (new)` marker allowed; `--names` values are checked by
  the existing `_forbidden` rule (newline, backtick).
- **Invariant of position (rule 11 (ii))**: the block never enters any manifest section's extent. It sits after the
  last header line behind a blank line (extents end at the first blank line, `dispatch_manifest.section_extent`,
  premise P2); its lines start with `readers:` or `- `, never with a manifest key or an id key (the kinds of §2.2
  collide with none of `KEY_GROUPS`, `task`, `node`, `feature`, `manifest-skip`, premise P2); it carries no numbered
  line (`designer_threshold` counts them) and no absolute path. So `check`, `owned_paths`, `given_paths`,
  `header_ids` and the designer count are identical with and without the block — held by the existing round trip
  `test_printed_text_passes_check_and_ids_read_back` (premise P3) once a CASES row carries a block, and by step 3
  live.
- `dispatch_gate.given_path_warn` reads paths on any line outside the checked sections (premise P15). A block path
  present on the base but absent from the launching working tree draws a GIVEN-PATH WARN — a WARN, never a refusal,
  and true (the launching checkout lacks the file). No change to dispatch_gate.
- **Docstring (review M8)**: the module docstring's "NO grammar of its own … Pure output: stdout only … these are the
  only rules of the generator's own" is rewritten in S1 to say: the generator appends the readers block of
  `tools/owns_readers.py` (data, not grammar), checks headers + block through `decide_full`, and replaces a refused
  block with the unknown line (step 4). Part of S1's DoD.

### 3.2 `dispatch_manifest.py` — a NOTE first, a refusal never in this spec

In `check_cut`, for a checked (builder or writing) dispatch that passes: if no unquoted line matches
`^readers:[ \t]*(\d+ outside owns|unknown)\b` (review M2), append to the notes exactly:

`READERS NOTE: this writing dispatch carries no readers: line -- run python -B tools/owns_readers.py --paths <owns>
(dispatch_new.py prints it) and keep its block, or write 'readers: unknown -- <reason>' when it cannot run.`

- Not a `KEY_GROUPS` item (F-5, decided): adding one changes `ITEMS`, the INCOMPLETE and UNCHECKED texts and the
  manifest-skip item list (premise P2) — that is the promotion step, taken on evidence.
- The door is a hand-typed `readers: unknown -- <reason>`, not `manifest-skip: readers -- ...`: `manifest-skip:`
  accepts only `ITEMS` names and an unknown item REFUSES the dispatch (premise P2 `_parse_skip_line`). The hand-typed
  line matches the regex and counts as an informed pass (FR-4). S-4.
- A degraded cut: no note (the UNCHECKED note already says nothing was checked).
- Both worlds (rule 11 (i)): before S2 lands no note exists and `dispatch_new` output carries a block anyway; after
  S2, the block's header line is what silences the note (§3.1 step 3).
- Order: S2 waits for S1 and for FG7-49 (it owns `tools/dispatch_manifest.py`, batch-7 line 72; status there read
  «ожидает» at draft time while the brief said "being edited" — §N.2; the Lead checks the row before launch).

**Promotion rule (rule 10 (d), review M6)** — defined on what is countable: the note becomes a refusal only when the
calibration count L7 shows two `failure_class: spec` rejects AFTER the note shipped whose dispatch text carried no
`readers:` line AND whose reject note names a fact the block would have printed (a quarantined file, an absent path or
name, a reader of an owned file) — the last part is the calibrator's reading; and only as a new spec node.

### 3.3 Who reads the block

- **builder**: never writes into a file marked `quarantined`; a `slow` owned test is named "judged by the batch canon"
  (builder-rules 7b); an `absent` given or owned path is a question returned before work; for every `names` line, keeps
  the reader green or returns "changes needed outside owns: <path>" and STOPS (a return, not an edit outside owns);
  a `more` count is not a duty — the builder may run `--readers` itself when its change alters a file's interface.
  The line goes into `plans/builder-rules.md` (L5).
- **critic (diff gate)**: reads the block as the starting list for question 3 (seams); a diff that breaks a listed
  reader without naming it is a finding.
- **critic (plan gate)**: §4.1. **designer**: §4.2.

---

## §4 The rule texts

### 4.1 The plan-gate question (home: `docs/tasks/critic-diff-brief.md`, F-6 (b), decided)

L1 adds, in the brief's first paragraph, one sentence (review M7 (i); the title has no other reader — Grep
`Standing brief for the critic` over the repo outside worktrees: the brief itself and the review only):
"Since t-897 it also holds the plan gate (section «The plan gate», item 13): a critic on a plan or a dispatch draft
answers item 13 and items 4 and 12." Then, as its own section after item 12 and before «What comes back»:

```
## The plan gate (critic on a plan or on a dispatch draft; CLAUDE.md rule 3)

13. **FACTS AND EDGES** (evidence: t-896, 65 `failure_class: spec` rejects of 11-16.11.2026 -- 42 found by the code
    critic, 4 by the plan critic). Each sub-question gets its own verdict line.
    (a) EDGES: for every limit, empty or absent input, pair of the spec's own requirements, and artifact the change
    brings into existence (both worlds) -- is the behaviour stated, with the invariant it protects (CLAUDE.md
    rule 11)? A silent one is a finding named by the requirement that creates it.
    (b) MEANING: restate in one line what each changed field, gate or refusal means after the change; a restatement
    that contradicts another section or the spec's own example is a finding.
    (c) PREMISES: critic.md rule 12 applies to a plan's premises as to a report's claims. A statement about existing
    code, files or data without a premise (command + output, or file:line + quote) is a finding; you do not supply
    it. Re-run ONE or TWO premises the plan rests on most; one that does not reproduce blocks.
    (d) READERS: the plan carries the block of `python -B tools/owns_readers.py --paths <files it touches> --names
    <names it changes>`. Do NOT re-grep, re-count or re-classify what the block prints (readers, quarantine, slow,
    presence, name hits): those are code's data (P27). Re-run the tool only when the block is missing or its base sha
    is not today's origin/main. Every line gets an answer in one of these forms -- a line with no answer is a finding:
      quarantined -> "case moved to keep file <x>" | "not edited: <why>"
      slow        -> "judged by the batch canon"
      absent      -> "merged first: <commit/branch>" | "path or name corrected to <x>" | "node waits for <node>"
      exists      -> "(new) dropped: the spec edits the existing <x>" | "renamed to <x>"
      names       -> "unchanged: <why>" | "changes in stream <X>" | "case moved to <keep file>"
      hot         -> "names passed: <list>" | "file-wide change: <why>"
      more        -> "interface kept: <why>" | "listed with --readers and answered below"
      unsearched  -> "searched by hand: <command, hit count>" | "n/a: <why>"
    Then the KNOWN MISSES of the tool's docstring, one line each:
      miss 1 (transitive)          -> for a package path, quote `scenario_walk.py --witness-for <path>`: it is the
                                      transitive list; for a forge path, "n/a: <why>" or one grep
      miss 2 (built path/name)     -> "n/a: <why>" or one grep
      miss 3 (pinned VALUE)        -> does the plan change a VALUE (a count, a key, a literal) pinned elsewhere? name
                                      the value and grep it on the base, with the hit count
      miss 4 (short stem)          -> "covered by the file-name search" or one grep for the stem
      miss 5 (out of scope prose)  -> "n/a: <why>" or one grep over docs/ plans/
      miss 6 (stale base)          -> "base <sha8> is origin/main: yes|no"
      miss 7 (common-word stem)    -> nothing owed: it over-counts, never hides
```

(a) adds no new duty — it makes rule 11's edges a plan-gate verdict line. (c) cites critic.md rule 12 instead of
restating it (review M7 (ii)); the "one or two" bound is the brief's cost ceiling.

Pointer in the critic role file (F-6 (b)): one line as rule 21 of `.claude/agents/critic.md` (today's last rule is 20,
critic.md:172):

```
21. On a plan gate, the facts-and-edges question with its own verdict lines: docs/tasks/critic-diff-brief.md item 13.
```

The critic exam owed by critic.md rule 10 (premise P16) is not runnable: `PROCESS/CRITIC_EXAM.md` is absent. Road
(review M5, the precedent commit `1f165a38`, t-847): the commit message records "Deviation: exam not run; debt F3-1".
F3-1 lives today at `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md:67`, status «ожидает» (moved
from forge/3 on 01.11.2026; the review's pointer to forge/3 is stale). That batch is TAKEN («в работе», line 3), so
its row text is frozen (PROJECT.md «Командная работа» п. 2); no row edit is made: F3-1's exam runs on the role text
current at its run, which then includes rule 21.

### 4.2 The designer line (home: `.claude/agents/designer.md`, appended to rule 3)

```
   The readers list is the block of `python -B tools/owns_readers.py --paths <touched files> --names <changed
   names>` (counts by default; `--readers` lists): you have no shell, so the Lead attaches it to the brief and the
   plan critic re-runs it on your touched-file list; quote the block and give every line its answer in the forms of
   docs/tasks/critic-diff-brief.md item 13 (d). A hand grep is owed only for what its KNOWN MISSES name.
```

The designer's `tools:` line is `Read, Glob, Grep, Write` (premise P17); F-8 (a), decided: the Lead attaches the block.

---

## §5 Tests (`docs/TESTING.md`: one parameterised test per behaviour, a world built once per file)

Witness scope: forge paths have no `scenario_walk.py --witness-for` row; the DoD names the test files that judge them
(CLAUDE.md rule 4). Home of T1: `tools/test_owns_readers.py` — the owner's word 17.11.2026 «да» to F-9 (a): a new
forge tool may have its own test file.

**T1 — the tool's table**, `tools/test_owns_readers.py`. ONE temporary git repo per file: a tiny tree with
`ai-packages/qa-factory/scripts/tests/` (a `test-layers.json` with keep and quarantine rows), a
`ai-packages/qa-factory/scripts/slow_tests.json` (valid shape per `_slow_tests_problem`: thresholds, `files` with one
name at `null` and one at 3 seconds — both slow by membership), `tools/`, one JSON carrier; committed;
`refs/remotes/origin/main` set by `git update-ref`; extra commits for the registry variants; one uncommitted file and
one untracked copy directory. The selftest module comes from the real checkout (§2.3 (ii)-s). One parametrized test
`test_owns_readers_table`, ids naming the case:

| id | input | expected |
|---|---|---|
| quiet | owned module + its only test both owned | exactly one line: `readers: 0 outside owns, 0 lines below -- ...` |
| count-default | owned module; 2 tests + 1 tool name it | header `3 outside owns`; one `- more:` line `2 test, 1 code`; no `outside` lines |
| readers-list | same, `--readers` | 2 `- outside: ... (test)` lines, namesake first; `- more: ... 1 code` |
| order-tiers | `--readers`; a namesake test, a test naming the file, a test with the stem only | that order |
| data-carrier | a JSON names the owned file | default: counted `1 data`; `--readers`: `- data: ...` |
| test-cap | 26 non-quarantined test readers, `--readers` | `hot` line + 25 `outside` lines + `more ... 1 test` |
| hot-with-names | the same, `--readers --names f` | no `hot`; no path `outside` lines; `more ... 26 test`; `names` lines for `f` |
| data-cap | 13 data carriers, `--readers` | 12 `data` lines + `more ... 1 data` |
| all-lifts | 26 tests + 1 code + 1 quarantined reader, `--all` | 26 test lines, the code line, the quarantined line; no `more` |
| quarantine-owned | owned test in quarantine | `- quarantined: ... (owned)` |
| quarantine-reader-count | a reader in quarantine | counted `1 quarantined` in `more`, never listed by default, never as plain test |
| quarantine-layers-absent | base without `test-layers.json` | header `quarantine: unknown (... absent ...)`; no `quarantined` line; `? quarantined` in `more` |
| quarantine-show-fails | monkeypatch `test_quarantine._git` → `(128, "")` for `show` | header `quarantine: unknown (... read empty)`; other lines printed |
| quarantine-malformed | `test-layers.json` blob not JSON | header `quarantine: unknown (... not JSON)`; other lines printed; no exception |
| quarantine-section-gone | keep present, no `quarantine` key | no quarantine line, no unknown segment |
| slow-owned | owned test listed at `null` seconds | `- slow: ... (owned)` (membership, not threshold) |
| slow-malformed | `slow_tests.json` without `thresholds` | header `slow: unknown (...)`; no `slow` line |
| absent-given | given file only in the working tree | `- absent: ... (given)` |
| new-exists / new-absent | owned `(new)` on / not on the base | `- exists: ...` / no line |
| untracked-copy | reader only in an untracked copy dir | not counted |
| names-hit | `--names f`; a test outside owns calls `f` | `- names: <test> (test) names f` |
| names-absent | `--names nosuch` | `- absent: name nosuch -- ...` |
| names-new-absent / names-new-exists | `--names "g (new)"` absent / present | no line / `- exists: name g (new) ...` |
| names-nonword | `--names --part` present in a file | found (no `-w`), no git option error |
| names-cap | 21 names | 20 searched; `- unsearched: 1 more names over the cap` |
| base-missing | `--base origin/nope` | Example C only; no count, no "not quarantined" |
| grep-rc-128 | monkeypatch `gitcmd.git` → rc 128 for `grep` only | header `readers: unknown -- git grep exited 128 ...`; `absent` line still printed; no `0 outside owns` |
| grep-timeout | the same with rc -1 | the same with `-1` |
| lstree-fails | monkeypatch rc 128 for `ls-tree` | `presence: unknown`; no `absent`/`exists`; quarantine and slow unknown |
| outside-repo | `C:/elsewhere/x.py` | `- unsearched: x.py (outside the repo; ...)`; no absolute path anywhere in the block |
| dir-small / dir-wide | a directory under / over 40 files | expanded / one `unsearched` line |
| short-stem | owned `s0.md`, a file saying "s0" | not a reader unless it names `s0.md` |
| space-cyrillic | owned `my dir/ф.py` named by a test | counted |
| dash-name | owned `-x.py` | searched, no git option error |
| empty-paths | `--paths` with a blank item only | exit 2, `OWNS_READERS REFUSED` |

The rows `quarantine-*` are ONE contiguous row group, deleted with `_quarantine_status` (§2.3 (ii)-q).
Outside-input battery (rule 11): magnitude (test-cap, data-cap, dir-wide, names-cap), nesting (dir-small), encoding
(space-cyrillic), broken/empty (empty-paths, base-missing, quarantine-malformed, slow-malformed, grep-rc-128),
injection (dash-name, names-nonword). Time: one world per file, well under 10 s.

**T2 — the dispatch junction**, rows in the existing CASES table of `tools/test_dispatch_new.py` (premise P3):
- `readers-block`: BASE with a real owned tools file → stdout holds the headers, a blank line, then a `readers:` line;
  the round trip `test_printed_text_passes_check_and_ids_read_back` runs on it unchanged. On a clone without
  `origin/main` the line is the unknown form — the assertion is on `readers: ` being present and the round trip.
- `readers-tool-raises`: monkeypatch `owns_readers.report` to raise → headers printed, `readers: unknown -- ...`, exit 0.
- `readers-no-note`: stderr carries no `READERS NOTE` (true trivially before S2, meaningful after: the row is written
  in S1 and kept).
- `block-refused`: monkeypatch `owns_readers.render` to return a text the manifest check refuses (vector:
  `manifest-skip: bogus -- x`, an unknown item, premise P2; the builder confirms the vector refuses by running the row
  before step 4 exists) → stdout headers + `readers: unknown -- the manifest check refused the block (...)`, stderr
  `OWNS_READERS: ...`, exit 0.
- `names-passthrough`: `--names "f (new)"` reaches `report` (monkeypatched spy).
- existing refusal rows keep `out == ""`.

**T3 — the note**, rows in `tools/test_dispatch_manifest.py`: builder dispatch without `readers:` → `READERS NOTE` in
the notes, exit 0; with `readers: 20 outside owns, 1 lines below -- ...` / `readers: unknown -- x` → no note; the
retired form `readers: ok -- ...` → the note; a `readers:` line inside a fence → the note; a critic dispatch without
owns → no note; a degraded cut → no note.

---

## §6 Phases, streams, owns, measurement, Lead edits

### Phase 1 — the cheapest version (§0)

**S1 — builder: the tool and its door**
```
owns:
C:/QAFactory/forge-repo/tools/owns_readers.py (new)
C:/QAFactory/forge-repo/tools/owns_readers.json (new)
C:/QAFactory/forge-repo/tools/test_owns_readers.py (new)
C:/QAFactory/forge-repo/tools/dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_new.py
```
given: this spec; `tools/gitcmd.py`; `tools/test_quarantine.py` (`_blob_sections`, `_git`, `_pkg_module`, `Unknown`);
`ai-packages/qa-factory/scripts/selftest.py` (`_slow_tests_problem`, `slow_tests` 975-1043);
`tools/dispatch_manifest.py`; `tools/dispatch_gate.py` (`decide_full`); `docs/TESTING.md`; `plans/builder-rules.md`.
non-goals: no change to dispatch_manifest.py, dispatch_gate.py, test_quarantine.py, selftest.py or any package file;
no fetch; dispatch_new prints the DEFAULT render (counts), never `--readers` (that is phase 2).
edges: §2.5 E-1..E-17; §3.1 steps 1-4 and the position invariant.
DoD: `python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py -q` green; one measured run
`python -B tools/owns_readers.py --paths tools/dispatch_manifest.py tools/test_dispatch_manifest.py --readers` and one
`python -B tools/owns_readers.py --paths ai-packages/qa-factory/scripts/story_run.py --names s0_criteria` with output
and wall time in the report (expected shapes: §2.4 rows 1-2); the tool's docstring carries KNOWN MISSES 1-7, the
`_blob_sections` runner exception, the removal line of (ii)-q and the §2.7 split; dispatch_new's docstring per §3.1
(M8).

**S2 — builder, after S1 and FG7-49 are merged: the note**
```
owns:
C:/QAFactory/forge-repo/tools/dispatch_manifest.py
C:/QAFactory/forge-repo/tools/test_dispatch_manifest.py
```
given: this spec §3.2, §5 T3; `tools/dispatch_manifest.py`; `tools/test_dispatch_manifest.py`.
non-goals: no `KEY_GROUPS` item, no change to `ITEMS`, the INCOMPLETE/UNCHECKED texts or `_parse_skip_line`.
edges: §3.2 (regex, fenced line, degraded cut, critic without owns, both worlds).
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py -q`
(test_dispatch_new.py for the `readers-no-note` row; test_dispatch_gate.py because the note travels through
`decide_full`). Before launch the Lead runs S1's tool on these owns and puts its block into the dispatch.

### Measurement — the gate between phase 1 and phase 2 (review B6; rule 10 (d))

- **M-1 (Lead; extraction may go to a scout)**: persist the t-896 per-line classification — every one of the 65
  `failure_class: spec` lines with its class (a1/a2/b/c/d/e) and its task's `delegated` worker_ref — as one file
  `docs/tasks/specs/reviews/t-896-spec-reject-classes.md`. This is the denominator's carrier; until it exists, any
  share of "the 30" is an estimate and says so.
- **M-2 (Lead, after S1 lands)**: for each code-fact reject (a1/e) of M-1, take the dispatch text from the worker
  transcript (`worker_ref` `agent:<id>`), run `python -B tools/owns_readers.py --paths <its owns> --given <its given>
  --names <names its spec changed> --base <the commit before the reject's fix> --readers`, and record per line:
  caught by the DEFAULT block (yes/no), caught by `--readers` only (yes/no), not caught. Result table appended to the
  M-1 file.
- **Promotion**: phase 2 opens only when M-2 shows at least two rejects caught by `--readers` and NOT by the default
  block (S-9). Otherwise the listing stays on demand and the result is written into the M-1 file as the reason.

### Phase 2 — conditional on M-2

**S3 — builder**: `dispatch_new` prints the `--readers` render. owns: `C:/QAFactory/forge-repo/tools/dispatch_new.py`,
`C:/QAFactory/forge-repo/tools/test_dispatch_new.py`; DoD: `python -m pytest tools/test_dispatch_new.py -q` with the
`readers-block` row asserting an `outside` line for a known reader. Specified then, from M-2's numbers (caps included).

### Lead edits (one commit with the mechanism block of CLAUDE.md rule 10 — one line for EVERY axis of
`docs/SIBLING_MAP.md`; the axes this touches, at least: 2 (exam instruments: the critic.md edit without an exam, F3-1),
9 (a forge "is this a test" reader, L8), 10 (a new gitcmd caller, and `_blob_sections`'s own runner, L8), 13 (the one
cut of a dispatch text: the block's position), 18 (in-tree ratchets — the tool reads them), 31 (one owner per role
aspect — the pointer row), 34 (one road: the §2.7 split and C6))

- L1 `docs/tasks/critic-diff-brief.md` — the first-paragraph sentence and the section of §4.1.
- L2 `.claude/agents/critic.md` — rule 21; the commit records the exam deviation on F3-1 (§4.1).
- L3 `.claude/agents/designer.md` — the §4.2 line.
- L4 `tools/tests/test_role_carriers_one_owner.py` — a POINTERS row `(".claude/agents/critic.md",
  "docs/tasks/critic-diff-brief.md item 13", BRIEF, "13. **FACTS AND EDGES**")` (premise P19).
- L5 `plans/builder-rules.md` — the builder's duty of §3.3 and the §2.7 split, beside 7b. It names NO package test
  file: `tools/test_quarantine.py` lists builder-rules.md among `FORGE_CARRIERS` (test_quarantine.py:51), and a carrier
  naming a test blocks that test's deletion.
- L6 CLAUDE.md rule 11 checklist point (5): one clause "for a writing dispatch: the `readers:` block of
  tools/owns_readers.py" — keeping every `install_parity_anchors.json` anchor of CLAUDE.md (premise P20).
- L7 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` — the detector of rule 10 (c), on countable data (review M6): per
  calibration, the `failure_class: spec` rejects of the window; for each, whether its dispatch text (worker transcript
  via `worker_ref`) carried a `readers:` line (the §3.2 regex), and whether the reject note names a fact the block
  prints (the calibrator's reading). Appended as a new check at the end; the file's two `install_parity_anchors.json`
  anchors kept; no package test file named (FORGE_CARRIERS, as L5).
- L8 `docs/SIBLING_MAP.md` — axis 9: a FORGE-reader paragraph for `tools/owns_readers.py` like the `tools/test_volume.py`
  one (classes by scope glob `test_*.py`; direction: a tool named `test_*` is counted as a test — over-report); axis 10:
  `owns_readers` added to the gitcmd callers ("nine callers" becomes ten) and `test_quarantine._git` named among the
  wrappers left on their own code (it is not listed today, §N.8).
- L9 C6 — a finding file in `plans/piles/forge/findings/` and its row in an untaken forge batch (PROJECT.md
  «Командная работа» п. 2): node "one answer to 'which tests concern this package path'": owns
  `tools/owns_readers.py` (and whatever F-11 decides); test: a row in `tools/test_owns_readers.py` asserting that for a
  package path the tool reports every keep file `--witness-for` names, or the convergence's own replacement; owner: the
  Lead of pile `forge`.
- L10 `docs/tasks/specs/td-15-scenarios-quarantine.md` §D.3 (the deletion condition's carrier, PROJECT.md package
  change item 2) — one line: "deleting the quarantine section also deletes `tools/owns_readers.py::_quarantine_status`,
  its `quarantined` kind, the `Q quarantined` part of `more` and the T1 rows `quarantine-*`; if `tools/test_quarantine.py`
  goes too, `_slow_status`'s loader moves first (F-13)".
- Supersede (Lead, 17.11.2026): L1, L2, L4, L5 superseded by t-1117/t-1133 (critic.md rule 24; the POINTERS row to rule 24 Q13; TESTING «Что запускать по своей правке» and builder.md rule 12); L3 lands as t-1133 card C3's designer.md rule 3 line, re-pointed to critic.md rule 24, Q13 (d); stream L writes no critic.md rule.

**Rule 10's four questions, short**: (a) cost — one tool run per writing dispatch (~0.2 s per grep, measured by the
critic), a default block of 2-3 lines plus up to 38 per name (§2.4), the builder's stop on a names line, one or two
premise re-runs per plan critic, one M-1/M-2 measurement; (b) axes — the commit block above; (c) detector — L7;
(d) on the path — `dispatch_new.py` prints the block, the launch hook's NOTE (C3) shows its absence; the plan-gate
question rests on discipline with L7 as its detector.

### 6.1 Readers of every touched file (designer rule 3)

Grep scope `tools/`, `.githooks/`, `.claude/` excluding `.claude/worktrees/`. Positive control for `.githooks/`:
`mechanism_gate\.py|SIBLING_MAP\.md` → `.githooks/commit-msg` 1 hit (the same call with `builder-rules\.md|SIBLING_MAP\.md`
→ 0).

| Touched file | Command (Grep tool) | Hits (outside worktrees) | Reader → status |
|---|---|---|---|
| `tools/dispatch_new.py` | `dispatch_new` over tools/ | 2 files (dispatch_new.py 3, test_dispatch_new.py 7) | test_dispatch_new.py → changes in S1 (T2) |
| | over .claude/ | `.claude/skills/next-task/SKILL.md:39` | unchanged ("lines from dispatch_new.py"; still true — the block follows them) |
| | over .githooks/ | 0 (control above) | — |
| `tools/owns_readers.py`, `.json`, `test_owns_readers.py` (new) | `owns_readers` -i over the repo outside worktrees | 2 files: this spec and review t-904 (positive control: the same call finds them) | dispatch_new.py → S1; `tools/*.json` scope row covers owns_readers.json itself (a self-hit, dropped as "inside owns" when owned) |
| `tools/dispatch_manifest.py` | the critic's hand run of the tool's own search (review item 2) | 20 outside S2's owns: 9 tests, 10 code, 1 data (`tools/warn_layers.json`) | all unchanged except test_dispatch_manifest.py (S2), test_dispatch_new.py (S1, T2); the note is additive, `check`'s 3-tuple keeps its shape; S2's dispatch carries the tool's block (§6 S2) |
| `docs/tasks/critic-diff-brief.md` | `critic-diff-brief` over tools/ | 3 files: install_parity_anchors.json 1, tests/test_role_carriers_one_owner.py 7, test_handoff_rule_anchors.py 1 | anchors of existing items unchanged (a first-paragraph sentence appended, a section inserted after item 12); test_role_carriers_one_owner.py → L4 |
| | title `Standing brief for the critic` over the repo | the brief + review t-904 | unchanged (title kept) |
| `.claude/agents/critic.md` | `critic\.md` over tools/ *.py,*.json | install_parity_anchors.json:139-140, test_role_carriers_one_owner.py, test_handoff_rule_anchors.py:33, dispatch_gate.py:65 (comment), critic_verdict.schema.json:5 | all unchanged (rule 21 appended; no anchor removed) |
| `.claude/agents/designer.md` | `designer\.md` over tools/ *.py,*.json | install_parity_anchors.json:168-169, test_role_carriers_one_owner.py:38/64-65, test_handoff_rule_anchors.py:36, journal_validator.py:162/349, mechanism_gate.py:668, test_journal_validator.py:801 (comments) | unchanged (a line appended inside rule 3) |
| `plans/builder-rules.md` (L5) | `builder-rules\.md` over tools/ | 9 files, 17 hits: fixtures/dispatch_manifest K3/K4/K7 (1 each), test_dispatch_manifest.py 1, tests/test_role_carriers_one_owner.py 5, test_handoff_rule_anchors.py 1, test_split.py 1, test_quarantine.py 1 (`FORGE_CARRIERS`), test_test_quarantine.py 5 | unchanged, provided L5 names no package test file (FORGE_CARRIERS) and removes no anchored text |
| `docs/SIBLING_MAP.md` (L8) | `SIBLING_MAP\.md` over tools/ *.py | 12 files, 23 hits: mechanism_gate.py 7 (reads axis HEADINGS), test_mechanism_gate.py 4, gitcmd.py 2 (points to axis 10), claim_control_gate.py 2, exam_runner, language_sites, negative_lint, test_language_sites, test_wiring_check, test_split, test_quarantine (`FORGE_CARRIERS`), tests/test_role_carriers_one_owner.py (1 each) | unchanged: L8 edits row text of axes 9 and 10, no heading; gitcmd.py's pointer stays true |
| `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` (L7) | `WEEKLY_CALIBRATION_PROTOCOL` over tools/ | 15 files, 36 hits (dispatch_gate 2, journal_validator 2, test_claim_control_gate 11, install_parity_anchors.json 2, test_handoff_rule_anchors 2, test_mechanism_gate(_md) 2+2, warn_density 2, journal_echo, hook_liveness_probe, test_dispatch_gate_md, test_journal_validator_merge, test_warn_density, test_quarantine 1 each, fixtures/host_pre_delivery_CLAUDE.md 5) | unchanged if L7 APPENDS a check and keeps both anchors; the Lead checks test_claim_control_gate's 11 references for a check-count pin before the commit (not read by me) |
| `docs/tasks/specs/td-15-scenarios-quarantine.md` (L10) | `td-15-scenarios-quarantine` over the repo | tools/test_quarantine.py 1 (names the spec path) and 24 docs/plans files | unchanged (a line appended to §D.3) |
| `tools/test_quarantine.py` (imported, not changed) | `_blob_sections` over tools/ | test_quarantine.py 3, test_test_quarantine.py 2 | unchanged; a rename of `_blob_sections`, `_pkg_module` or `Unknown` now breaks owns_readers — S1's docstring names the imports |
| `ai-packages/.../selftest.py` (imported, not changed) | — | `_slow_tests_problem` and `slow_tests` | unchanged; a rename breaks `_slow_status` → `slow: unknown` (E-14), never a wrong fact |
| `test-layers.json`, `slow_tests.json` (read only) | — | — | unchanged |
| `.claude/agents/critic.md` exam row `plans/piles/onboarding-forge/batch-2-...md:67` | — | — | unchanged (frozen batch; §4.1) |

---

## F. Forks

Decided forks (the Lead, 17.11.2026, with the review's corrections; the owner where noted):

- **F-1 Search base** — (a) `origin/main` via `git grep <sha>`. Decided.
- **F-2 `--names`** — (a) optional on the tool and on `dispatch_new`; plus the `hot` line asking for it (review). Decided.
- **F-3 Data carriers** — (a) scope globs, no list. Decided.
- **F-4 Name presence** — (a), widened by review B2: hits printed as `names` lines, a `(new)` marker for names. Decided.
- **F-5 Note mechanics** — (a) a presence regex, not a section. Decided.
- **F-6 Home of the plan-gate rule** — (b) brief section + critic.md rule 21 + the L4 row; the exam deviation on F3-1
  (review M5). Decided.
- **F-7 slow_tests.json reader** — CHANGED by review B5: read through the one reader's validator
  `selftest._slow_tests_problem` with MEMBERSHIP semantics; the old (a) "parse it, threshold" is withdrawn. Decided.
- **F-8 The designer and the shell** — (a) the Lead attaches the block. Decided.
- **F-9 Test file** — (a) `tools/test_owns_readers.py`; the owner's word 17.11.2026 «да» (a new forge tool may have its
  own test file). The fallback into test_dispatch_new.py is dropped. Decided.
- **F-10 Cap values** — replaced by §2.4 (tests-first, test_cap 25, data_cap 12, counts for code and quarantined
  readers, directory 40). Decided with the review's fix.

Open forks (new in this round):

- **F-11 Where the witness-for / owns_readers split is stated (review M9 asks: both docstrings).** (a) the tool's
  docstring + `plans/builder-rules.md` 7b (L5), NOT `scenario_walk.py` [recommended: the package ships to other
  projects without `tools/` (PROJECT.md «Релиз»: the copy is `ai-packages/qa-factory/` only), so a package docstring
  naming a forge tool points at a file the reader does not have — AR-4's spirit, the same reason
  `test_quarantine.forge_texts` gives: "the package does not read docs/, AR-4"; `--witness-for`'s rule text already
  lives in builder-rules 7b, the forge carrier]; (b) also one sentence in `scenario_walk.py`'s docstring ("which tests
  must not break is a forge question, outside this package") — a package change: an `architecture:` line (AR-15 kept),
  `selftest --lang`, a fourth stream. The review's M9 is applied under (a); (b) costs one package commit.
- **F-12 The phase boundary (the Lead's "is the cheapest version enough", review item 8).** (a) phase 1 COMPUTES the
  reader list and prints COUNTS by default; `--readers` lists it (B1's tests-first caps), used on demand and by M-2;
  phase 2 = `dispatch_new` prints `--readers` after M-2 [recommended: one code path, the measurement runs the very
  rendering it would promote, and B1's order is built and tested now]; (b) phase 1 has no reader computation at all
  (presence, layers, names only); phase 2 builds the list after a hand-scripted M-2 [smaller S1, but M-2 then measures
  a script, not the tool]; (c) no phases: `dispatch_new` prints the `--readers` form now [the original plan; contradicts
  B6's "unproven"].
- **F-13 How `_slow_status` loads the selftest module.** (a) `test_quarantine._pkg_module(root, "selftest")` — the one
  existing forge road for loading a package module, a named dependence; L10 says it moves first if the quarantine
  deletion removes `tools/test_quarantine.py` [recommended]; (b) a local 6-line `importlib` loader in owns_readers —
  independent of test_quarantine, but a second loader beside `_pkg_module` (a clone the ratchet may flag, AR-15).

## S. Small choices I closed

- S-1 Repo-relative forward-slash paths in the block; an outside path by base name only (keeps the block out of
  `owned_paths` and absolute-path readers).
- S-2 Scope globs (with `:(glob)` magic) and caps (`test_cap` 25, `data_cap` 12, `dir_cap` 40, `names_cap` 20) live in
  `tools/owns_readers.json` (FR-13 analog: closed variety in data).
- S-3 Stems under 4 characters are searched by file name only.
- S-4 Until promotion, the note's door is a hand-typed `readers: unknown -- <reason>` (`manifest-skip:` refuses an
  unknown item name, premise P2).
- S-5 `dispatch_new` imports the tool (no subprocess); the tool reaches git through `gitcmd.git` except the `git show`
  inside `_blob_sections`, which runs `test_quarantine._git` (corrected, review M4).
- S-6 No fetch; the header prints the searched sha.
- S-7 Listing order: namesake tests (`test_<stem>*`), then files naming the full file name, then stem-only hits;
  alphabetical within. (It puts line 829's `test_selftest_shard.py` and `test_selftest_slow_tests.py` first for an
  owned `selftest.py`.)
- S-8 A name with a non-word character at either end is matched as a plain fixed string, without `-w`.
- S-9 Promotion threshold for phase 2: two rejects caught by `--readers` only — the same "two rejects" bar as the
  note's promotion rule (§3.2). The Lead may set another.
- S-10 The selftest module is loaded from the tool's own checkout, the blob from `--repo` at the base: the validator
  is code of the running forge, the data is the base's.
- S-11 The brief keeps its title; one first-paragraph sentence names the plan gate (review M7 (i) offered either).

## R. Replay — would PART 1's output have shown the fact? (corrected by review B6)

| Line | Fact missed | Shown? | Why |
|---|---|---|---|
| 384 (t-133), 397 (t-134) | node tests written into quarantined files | **yes (likely)** | (ii)-q on an owned/given test; owns not rebuilt by the critic or me — taken from the notes |
| 1060 (t-420) | DoD sent rows to a quarantined file | **yes (likely)** | same |
| 1115 (t-439) | `test_import_test_receipt.py` edited while quarantined | **yes** | in `quarantine` at origin/main (the critic parsed the blob: True) |
| 541 (t-199) | `require_project_at` only on unmerged batch-1 | **yes with `--names`** | (v): `absent: name` — only if the dispatcher passes the name |
| 1395 (t-559) | test_conductor_doors.py red outside owns | **yes only with `--names s0_criteria`** | at `3e8a085d~1` the test names neither `driver_s0` nor `ticket_adapter` (control: 8 readers of `driver_s0`); it names the method `s0_criteria` (:760) — review B2 |
| 1117 (t-442) | frozen dict pins `qa-retro-analyst 14075` | **yes only with `--names qa-retro-analyst`** | KNOWN MISS 3; the pin is gone today (Grep `qa-retro-analyst\|14075` → 0, control `role-load` → 1) |
| 1181 (t-462) | analyst ratchet red outside owns | **no for t-462** | an integration of branches; the red came from t-437's earlier merge (journal 1180); a `data` count could have helped t-437 if it owned the role file |
| 294 / 307 (t-113) | 99 fixture inputs lack the new key | **no new information** | the reader tests were already in the DoD run ("100 failed"); the miss is a temporal edge — PART 2 (a) |
| 829 (t-325) | selftest imports hooklib; two tests red | **default: no; `--readers`: listed** | default: counted (106 readers, `hot`); `--readers`: first two lines by S-7; the cause (selftest.py:93 rule) is a2 — PART 2 (c) |
| 417 (t-148), 551 (t-202) | a signature / a field's content | no | a2; PART 2 (c) |
| 1972 (t-803) | `--part exits:<group>` does not exist | partial | `--names "exits:"` reports `absent` only if the string is absent in the whole tree |
| 2172 (t-885) | 12 red tools tests after the landing | partial | the source pins name their tools → counted; the Linux exec bit → no (class c) |

Firm catches of phase 1: the 4 quarantine rows and 541 (with the name); 1395 and 1117 with the right name. The literal
reader list: zero firm catches among the replayed rows. **The share of the 30 code-fact rejects it would catch is
unknown** — the 30 have no carrier (M-1 creates one; M-2 measures).

## N. Noticed contradictions and analogs (not widened)

1. The brief names `tools/ratchet-files.json` as a carrier: it does not exist (draft trail: Glob `tools/*.json` → 12
   files, none of that name; control `**/dup-baseline*` → found).
2. The brief said FG7-49 is "being edited now"; `plans/piles/forge/batch-7-vhodyashchie-4.md:72` read «ожидает» at
   draft time.
3. critic.md rule 10 requires `PROCESS/CRITIC_EXAM.md`; absent. Its debt F3-1 moved from forge/3 to
   onboarding-forge/2:67 on 01.11.2026 (review M5 pointed at forge/3).
4. `test-layers.json` note (line 3) says "Read only by scripts/selftest.py test_layers()", while
   `tools/test_quarantine.py::_blob_sections` reads it at a revision — an existing second reader this spec reuses.
5. `scenario_walk.py --witness-for` vs this tool — now node C6 (L9) and fork F-11, no longer a free residual.
6. FG7-53 ("owns judged at worker stop", batch 7) works on the same owns lists; the Lead checks its row before launch.
7. Designer rule 3's own grep drowns in `.claude/worktrees/` copies; the same base-tree search would help it.
8. `tools/test_quarantine.py::_git` is a git wrapper on its own code that SIBLING_MAP axis 10 does not list among
   "the git wrappers left on their own code" (axis 10 row "the one git runner", SIBLING_MAP.md:266) — L8 names it.
9. (review M11) `docs/tasks/critic-diff-brief.md:11-12` still says "until `scripts/tests/test-layers.json` holds
   quarantine rows" while the section holds 431 rows — a stale clause for the Lead's queue (L1 touches the same file;
   fixing it there is the Lead's call, not part of this spec).
10. The `.claude/worktrees/read-main` checkout named by the local memory note does not exist on this machine; my
    reads of code were of the root checkout — the critic read the same line ranges at origin/main (review trail) and
    they agree with mine.

## T. Reading trail (premises)

- P1 `tools/dispatch_new.py` read whole (this round): docstring 1-17; `build_text` 77-98; `_ids_refusal` 101-109;
  `main` 112-151 (`decide_full(payload)` on the header text, notes to stderr 147-149).
- P2 `tools/dispatch_manifest.py` (draft round, read whole): KEY_GROUPS 84-93; ITEMS 94; texts 137-163; PATH_CAP 189;
  section_cut 319-374; section_extent 613-621; `_parse_skip_line` 257-275; `_IDS_HEADER_RE` 750; designer_threshold
  859-871; check_cut 905-970.
- P3 `tools/test_dispatch_new.py` read 1-119 (draft round): CASES 42-73; refusal prints nothing 84-85; round trip 99-118.
- P4 `.claude/agents/critic.md`: rules 12 (70-83), 19 (163-171), 20 (172-177, the last rule). P5 `docs/TESTING.md`
  (draft round).
- P6 `tools/test_quarantine.py` (this round): `Unknown` 66-67; `_pkg_module` 88-109; `_git` 116-122 (own subprocess,
  timeout 120, exception → `(128, "")`); `_blob_sections` 208-217 (rc ≠ 0 → empty sections; bad JSON → `Unknown`);
  `FORGE_CARRIERS` 51.
- P7 (corrected) `ai-packages/qa-factory/scripts/selftest.py`: `SLOW_TESTS_FILE` 103; `fast=True skips the files
  scripts/slow_tests.json names` 868; `_slow_tests_problem` 975-997; `slow_tests` 1000-1043 ("The one reader of
  scripts/slow_tests.json"; membership: "between the two it keeps whatever it has"). The draft's P7 ("no reader") was
  wrong: it grepped `SLOW_TESTS\b`.
- P8 `tools/gitcmd.py` read whole: `git()` 38-48 (`-c core.quotepath=false`; OSError/SubprocessError → rc -1);
  callers enumerated on axis 10 (docstring 7).
- P9 Glob `**/dup-baseline*` → 68 paths, 67 under `.claude/worktrees/` (draft round).
- P10 Glob `tools/test_*.py` lists `tools/test_quarantine.py`, `tools/test_split.py` (tools).
- P11 `scenario_walk.py:887-922` `witness_for` (draft round; the critic re-read 887-927).
- P12 `tools/source-split-carriers.json:3,14-31`. P13 `references/role-load.json:22,36`.
- P15 `tools/dispatch_gate.py:938-977` (this round): `find_missing_given_paths` "any line"; `given_path_warn` "OUTSIDE
  the checked sections", a WARN text.
- P16 critic.md:58-63 (rule 10). P17 designer.md:5. P18 critic.md:5.
- P19 `tools/tests/test_role_carriers_one_owner.py:53-68` POINTERS. P20 `tools/install_parity_anchors.json`.
- This round also: `docs/tasks/critic-diff-brief.md` headings (items 1-12 at 27-83, «What comes back» 97, title line
  1); `docs/SIBLING_MAP.md` axis headings 44/232/254/317/393/471/590 and axes 9-10 bodies 232-271;
  `tools/mechanism_gate.py:211-236` (MECHANISM_PREFIXES: `docs/SIBLING_MAP.md`, `PROCESS/`, `.claude/agents/` are
  mechanism paths; `tools/owns_readers.py` is not); `plans/piles/onboarding-forge/batch-2-onboarding-roles-forge-p3.md`
  1-20 and :67; `plans/piles/forge/batch-3-exam-debts.md:24`; Grep `dispatch.record` in tools/ (journal_hooks.py:2 —
  the dispatch record writes `delegated` with a brief note, not the dispatch text: hence L7 reads transcripts).
- Review t-904 read whole; its counts (22/254/106 files, 81 quarantined, 0.2 s) are used as the critic measured them,
  not re-run (the designer has no shell).

needed beyond the manifest: the files in the trail other than the two given.

## Decisions and the owner's words this spec rests on

- The Lead, 17.11.2026: the fork decisions listed under F (decided), with the review t-904's corrections accepted as
  written; the Lead's choices on B1-B6 given in dispatch t-913.
- The owner, 17.11.2026 («да» to the Lead's recommendation on F-9): a new forge tool may have its own test file.
- The owner, 17.11.2026, NOT decided: «карантин это временная мера. Может будет проще удалить все тесты что сейчас в
  карантине чтобы таких проблем не возникало?» — the Lead recommends one watch run first, then deletion on her word.
  This spec keeps the quarantine line as one isolated function and one row group, deleted with the section (§2.3
  (ii)-q, L10).

## Fix round 1 (t-913) — review t-904

| Finding | What changed | Section |
|---|---|---|
| B1 cap + order hid load-bearing readers | Tests first, namesake/file-name/stem tiers; all test readers listed up to `test_cap` 25; code and quarantined non-owned readers as counts in one `more` line per subject; data up to 12; `hot` line asking for `--names`; worst-case sizes stated for dispatch_manifest (default 2-3 lines, `--readers` 12) and story_run (default 3, `--readers` 40) | §2.2, §2.4, S-7 |
| B2 names hits had no shape; new names read absent | `names` kind under the same caps; ` (new)` marker for names: absent → nothing, present → `exists`; presence over the whole tree | §2.1, §2.2, §2.3 (v), E-5, E-17, T1 names-* |
| B3 unknown could read as pass | rc map (grep 0/1/other; others 0/other); registry presence from the tool's own `ls-tree`; `quarantine: unknown` on absent / empty read / `Unknown`; the rest of the block kept; T1 rows grep-rc-128, grep-timeout, quarantine-show-fails, quarantine-malformed, lstree-fails | §2.2 Example D, §2.3, E-3b/c, E-15, E-16, T1 |
| B4 note fired on the generator's own run | `dispatch_new` builds the block first and passes headers + block to `decide_full`; refused-block fallback; T2 rows readers-no-note, block-refused | §3.1, §3.2, T2 |
| B5 slow reader exists; meaning is membership | `_slow_status` via `selftest._slow_tests_problem`, membership in `files`, no threshold; P7 corrected; F-7 changed | §1, §2.3 (ii)-s, T, F-7 |
| B6 replay overstated, yield unproven | §R corrected row by row; §0 states the reader list's yield is unproven; M-1 (persist the classes) and M-2 (replay on the 30 rejects) added; promotion only on M-2; cheapest version made phase 1 (fork F-12 on the boundary) | §0, §R, §6 Measurement, Phase 2, F-12 |
| M1 pathspec semantics | `:(glob)` for every scope row, `:(exclude,glob)` for exclusions; `ls-tree` literal paths only | §2.3 |
| M2 verdict words in the header | `readers: <R> outside owns, <L> lines below ... (literal mention; known misses ...)`; C3 regex `(\d+ outside owns\|unknown)`; T3 updated | §2.2, §3.2, T3 |
| M3 absolute path from E-4 | outside path printed by base name; T1 outside-repo asserts no absolute path | §2.2, E-4, T1 |
| M4 axes 2, 9, 10; S-5 false | axes listed in the Lead commit; L8 edits axes 9 and 10; S-5 names `_blob_sections`'s own `_git` | §2.1, §6 Lead edits, L8, S-5, §N.8 |
| M5 exam deviation road | the commit records "debt F3-1"; F3-1 located at onboarding-forge/2:67 (taken batch, row frozen, no edit); the "recorded as not runnable" form dropped | §4.1, F-6, §N.3 |
| M6 detector class has no carrier | detector and promotion rule defined on countable data: spec rejects × `readers:` line in the dispatch text (worker transcript); class reading stays the calibrator's | §3.2, L7 |
| M7 rule text | brief first-paragraph sentence; (c) cites critic.md rule 12; (d) concrete answer forms per kind and per known miss; "do not re-derive what the block carries" | §4.1, §4.2, S-11 |
| M8 dispatch_new docstring contract | docstring rewrite in S1's DoD | §3.1, §6 S1 |
| M9 two answers for package paths | split stated in the tool's docstring and builder-rules 7b; node C6 with owner and test (L9); package docstring returned as fork F-11 (recommended: not in the package) | §1 C6, §2.7, L5, L9, F-11 |
| M10 uncapped kinds, wrong cost claim | caps or counts for every kind; "1-15 lines" withdrawn; sizes from measured counts | §2.4, §6 four questions |
| M11 stale clause in the brief (side observation) | listed for the Lead's queue, not edited by this spec | §N.9 |
| Owner F-9 «да» | T1 home `tools/test_owns_readers.py`; fallback dropped | §5, F-9 |
| Owner quarantine question (open) | quarantine as one isolated function + one row group, deleted with the section; both worlds stated; L10 on the deletion carrier | §2.3 (ii)-q, E-3d, T1, L10 |
| Superseded statements | the old "Lead decisions" and "owner's word" blocks replaced by "Decisions and the owner's words"; old Examples A/B (`ok`, `to act on`), the 12/40 flat caps, the threshold slow rule, the "1-15 lines" claim and the F-9 fallback removed | whole file |

## The owner's word 17.11.2026 on the measure

«ок» to the Lead's statement of what the mechanism must remove: rejects of the class "the spec states a wrong fact
about the code" (30 of 65 in the week 11-16.11, scout t-896). M-1/M-2 judge it by that class and no other.
