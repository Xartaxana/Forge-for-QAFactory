# Spec facts by code, spec judgment by the plan critic (t-897, F19) — DRAFT

Designer draft from the Lead's intent brief (t-897). Forks are returned (section F), never decided. Status: draft,
awaiting Lead acceptance; critic on plan is owed (the draft carries forks, CLAUDE.md rule 3).

Evidence the brief rests on: scout t-896 (accepted), carrier `logs/journal/dev1.jsonl`, 65 lines with
`"failure_class":"spec"` 11-16.11.2026. I did not re-count the 65; I re-read 18 of the cited lines (trail, section T).

---

## §0 The Lead's reading, checked against the evidence

The Lead's reading: classes a, e, c are DATA about the repo (belong to code, P27); b, d are judgment (belong to a
critic rule). What the re-read lines show:

- **Class a splits in two.** (a1) *who else reads or pins the changed thing* — lines 1117, 1181, 1395, 453, 294,
  307, 829, 863, 1009, and the quarantine lines 384, 397, 1060, 1115. This IS data: a search over the tree answers
  it, and PART 1 is built for it. (a2) *what the existing code actually does* — line 417 ("value() has no element
  arg"), 551 ("my spec assumed an install signature in the receipt; it has none"), 1972 ("--part exits:<group> does
  not exist"), 829's second half ("Spec missed selftest's no-hooklib rule (:93)"). No reader list shows a missing
  argument, a field that is not there, or a rule written inside the changed file. a2 is closed by a PREMISE (command
  + output, file:line + quote) that the plan critic spot-runs — PART 2 (c), not PART 1. Partial help for a2 from code
  is fork F-4 (name presence on the base).
- **Class c is not data the tool can see.** The 16.11 landing (journal line 2172, t-885: "wave hook exec bit on
  Linux") is an environment fact (file mode on another OS); PART 1 does not claim it.
- **Class e (owns/ownership)** is data when it is "a test outside owns pins the old state" (PART 1 (i)/(iii)) and
  when it is "the node rests on an unmerged branch" (PART 1 (iv), only for PATHS; line 541 is a FUNCTION on an
  unmerged branch, so (iv) alone misses it — F-4 again).
- **b and d are judgment** — agreed; PART 2 (a)/(b).

So the direction holds with one correction: PART 2 carries a third duty besides edges and meaning — the PREMISE for
every statement about existing code — because a2 is the biggest share of class a that PART 1 cannot reach.

---

## §1 What changes, and the owner each check serves

| # | Change | Owner served (P27) | Census class |
|---|---|---|---|
| C1 | New forge tool `tools/owns_readers.py`: for given/owned paths prints readers inside/outside owns, layer status of test files (quarantine, slow), data carriers naming the path, presence on the base ref | **data (code)** — it gathers facts, decides nothing; it never says "the spec is complete" | n/a — a forge tool, not a package check; `judgment-census.json` covers `ai-packages/` only |
| C2 | `tools/dispatch_new.py` prints the tool's block after the header lines | data (code) | n/a (forge) |
| C3 | `tools/dispatch_manifest.py` adds a NOTE (never a refusal) when a writing dispatch carries no `readers:` line | data (code): presence of a line only | n/a (forge) |
| C4 | Plan-gate question for the critic (edges, meaning, premises, readers) | **judgment (a role — the critic), accepted by the Lead** | n/a (role text) |
| C5 | One line in `.claude/agents/designer.md` rule 3: the readers list comes from C1's output | judgment (designer), accepted by the Lead | n/a |

**AR-n**: this spec changes no file under `ai-packages/qa-factory/` — `architecture: none -- forge tools and role
texts only`. It READS two package files (`scripts/tests/test-layers.json`, `scripts/slow_tests.json`). For the first,
the spirit of AR-13 (a fact with a reader function is read only through it) is kept by reusing the forge's existing
revision reader `tools/test_quarantine.py::_blob_sections` (premise P6), not by parsing the file a second time.
`slow_tests.json` has no reader function that reads at a revision (premise P7); C1 parses its `files` and
`thresholds.slow_over_s` itself — named as a second reader here and in fork F-7.

---

## §2 The tool `tools/owns_readers.py`

### 2.1 Inputs

```
python -B tools/owns_readers.py --paths <p>... [--given <p>...] [--names <n>...] [--base <ref>] [--repo <dir>] [--all]
```

- `--paths`: owned paths (absolute or repo-relative; a trailing ` (new)` marks a new file, the same marker
  `dispatch_new.py` uses, premise P1). At least one; empty → exit 2 with a door (§2.5 E-1).
- `--given`: given paths — checked for presence on the base only (iv); readers are not searched for them.
- `--names`: optional names the spec changes (functions, keys, flags, constants). Their search is fork F-2/F-4.
- `--base`: the tree searched; default `origin/main` (fork F-1). `--repo`: the repo root; default the parent of
  `tools/`. `--all`: lift the per-path reader cap (§2.4).

Python API (what `dispatch_new.py` calls): `report(paths, given=(), names=(), base="origin/main", repo=None) ->
Report` and `render(report, all_=False) -> str`. Pure except for git reads through `tools/gitcmd.git` — "the one git
runner of the tools" (premise P8). Writes nothing.

### 2.2 Output — exact shape

One header line `readers: ...`, then at most one line per finding, each starting `- <kind>:`. Paths are
REPO-RELATIVE with forward slashes (never absolute — see the invariant in §3.1). Kinds, in this order:
`outside` (a reader outside owns), `quarantined`, `slow`, `data` (a carrier naming the path), `absent` (not on the
base), `exists` (marked new but on the base), `unsearched` (outside the repo / directory too wide / cap reached).

**Example A — nothing to act on** (every reader is itself owned):

```
readers: ok -- base origin/main 26dcf3d6; 2 owned, 3 readers, all inside owns
```

**Example B — three findings**:

```
readers: 3 to act on -- base origin/main 26dcf3d6 (tools/owns_readers.py; blind spots in its docstring)
- outside: tools/test_dispatch_gate.py (test) names tools/dispatch_manifest.py
- quarantined: ai-packages/qa-factory/scripts/tests/test_import_test_receipt.py (owned) -- the canon does not run it; a case goes to a keep file
- absent: docs/tasks/specs/x-spec.md (given) -- not on origin/main 26dcf3d6; a worktree builder cannot read it
```

**Example C — the base cannot be read** (FR-59: an unknown is never a pass):

```
readers: unknown -- base origin/main does not resolve here (git: <first line>); nothing was searched
```

The header's count is the number of `- ` lines. The sha is the base commit actually searched, 8 hex.

### 2.3 How each fact is computed

All searches run on the BASE TREE through `git grep`, not on the working tree (fork F-1). Reason, measured: the
working tree of this clone holds full repo copies under `.claude/worktrees/` (Glob `**/dup-baseline*` returned 68
paths, 67 of them under worktrees, premise P9) and an uncommitted state of other sessions; `git grep <ref>` sees
neither.

**Search scope** (data, not code — kept in `tools/owns_readers.json`, small choice S-2):
- tests: `ai-packages/qa-factory/scripts/tests/**/test_*.py`, `tools/test_*.py`, `tools/tests/**/test_*.py`;
- code: `tools/**/*.py` (non-test), `ai-packages/qa-factory/scripts/**/*.py` (non-test), `.githooks/*`,
  `.claude/settings*.json`, `.claude/hooks/**`, `.claude/agents/*.md`, `.claude/skills/**/SKILL.md`;
- data: `tools/*.json`, `ai-packages/qa-factory/references/*.json`, `ai-packages/qa-factory/scripts/*.json`,
  `ai-packages/qa-factory/scripts/tests/*.json`, `ai-packages/qa-factory/scripts/tests/fixtures/*.json` (top level
  only), `ai-packages/qa-factory/design/*.json`, `ai-packages/qa-factory/scripts/audit_factory.py` (the py-tuple
  ratchets of critic-diff-brief item 9).
- excluded: `scripts/tests/fixtures/stories/**`, `fixtures/run-*/**` (saved run copies name every script),
  `logs/`, `docs/`, `plans/`, `experiments/`.

The tests/code/data class comes from the scope row that matched (a file in two rows takes the first: tests, then
data, then code). Known misclassification: `tools/test_quarantine.py` and `tools/test_split.py` are TOOLS whose
names start with `test_` (premise P10) — they are listed as "test". Error direction: over-report (a tool shown as a
test reader), never a reader dropped.

**(i) Readers.** For each owned path, the search patterns are: its file name (`dispatch_manifest.py`,
`role-load.json`) as a fixed string, and its STEM as a whole word (`-w`) when the stem has 4 or more characters
(`dispatch_manifest`, `role-load`). One call for all owned paths:
`git grep -I -o -w -F -e <pat1> -e <pat2> ... <base> -- <scope pathspecs>`; each hit is attributed to the owned path
whose pattern it matched. A hit inside the owned file itself is dropped; a hit inside another owned file counts as
"inside owns" (counted in the header, not listed); every other hit is an `outside` line, one per reader file (the
first owned path it names; extra names are joined `names a.py, b.py`).

Search method name: **literal mention** (file name or stem word) on the base tree. Its blind spots, written into the
tool's docstring as KNOWN MISSES (the plan critic's duty starts there, §4):
1. transitive readers — a test that imports `a`, which imports the owned `b`, is not listed (`scenario_walk.py
   --witness-for` follows the package's import closure for scenario tests, premise P11; the DoD keeps naming it);
2. a path built from pieces (`Path("references") / name`), a name read from data, `importlib` with a computed string;
3. a pin on a VALUE without the file name — line 1117: a frozen dict pinning `qa-retro-analyst 14075` (§R);
4. stems under 4 characters (`s0.md` is searched by `s0.md` only);
5. readers outside the scope (docs, plans — prose readers are the designer's own walk);
6. a stale base: the tool does not fetch; the header prints the sha it searched.

**(ii) Layer status of test files.** For every owned or given path under `ai-packages/qa-factory/scripts/tests/`,
and for every `outside` reader there: quarantine = the file's base name is a key of the `quarantine` section of
`test-layers.json` at the base, read by `tools/test_quarantine.py::_blob_sections(root, base)` (premise P6); slow =
its base name is a key of `files` in `ai-packages/qa-factory/scripts/slow_tests.json` at the base with seconds over
`thresholds.slow_over_s` (premise P7). An OWNED or GIVEN test in quarantine or slow → its own line. An `outside`
reader in quarantine → its line says `(quarantined: the canon does not run it; do not edit)` instead of `outside`
(it cannot turn the canon red, but a builder must not write into it — lines 384, 397, 1060, 1115). Forge tests
(`tools/`) have no layer registry: no status is printed for them, and the docstring says so.

**(iii) Data carriers.** The `data` rows of the scope in (i): a hit there is a `data` line ("names it"). This covers
the registries keyed by file name (`tools/source-split-carriers.json` `carriers`, premise P12), the ratchets of
critic-diff-brief item 9 that live in JSON or `audit_factory.py`, `references/role-load.json` (keyed by role name =
the stem of the role file, premise P13), `tools/install_parity_anchors.json`, `tools/warn_layers.json`. No carrier
LIST is kept: a new ratchet under a scope glob is covered without an edit (fork F-3).

**(iv) Presence on the base.** One `git ls-tree -r --name-only <base> -- <paths>` call. Given or owned (not new)
path absent → `absent`. Owned `(new)` path present → `exists` ("marked new but already on the base"). Owned `(new)`
absent → nothing (expected).

### 2.4 Limits and performance

- Reader cap per owned path: 12 `outside` lines; beyond → one line `- unsearched: N more readers of <path> (run
  with --all)`. Invariant: a capped list is never presented as complete — the overflow line is always printed.
  Measured need: `selftest` is named in 56 package test files (premise P14); without a cap one owned `selftest.py`
  floods the dispatch.
- Directory in owns: expanded to the tracked files under it at the base (`git ls-tree`), at most 40; beyond →
  `- unsearched: <dir> holds N files; readers not computed -- name the files`.
- Path count: the tool takes at most `dispatch_manifest.PATH_CAP` (200, premise P2) paths; more → the rest are named
  in one `unsearched` line.
- Time: target under 5 s for 20 owned paths on this repo — **estimate, not verified** (the designer has no shell).
  The builder's report carries one measured run (wall time printed by the shell) on three real owns; wall time is
  never asserted in a test (FR-31). A git call that exceeds `gitcmd`'s timeout → Example C form with the reason.

### 2.5 Edge behaviour, each with its invariant

| E | Input | Behaviour | Invariant it protects |
|---|---|---|---|
| E-1 | `--paths` empty or all items blank | exit 2, stderr `OWNS_READERS REFUSED: no path given -- pass --paths <owned path>...` | the tool never prints `readers: ok` about nothing |
| E-2 | base ref does not resolve / git missing / git timeout | exit 0, Example C line only | an unknown never reads as "no readers" or "not quarantined" (FR-59); `_blob_sections` returns empty sections on ANY git error (premise P6), so the tool resolves the base with `rev-parse` FIRST and never calls it on an unresolved base |
| E-3 | `test-layers.json` absent at the base | the header carries `quarantine: unknown (test-layers.json absent at <sha>)` once | absence of the registry is never read as "not quarantined" |
| E-4 | path outside the repo root | `- unsearched: <path> is outside the repo` | a path the tool cannot search is named, never dropped |
| E-5 | new file `(new)` | (iv) inverse; readers searched by its name anyway (a test may already name it) | a "new" file already on the base is named (a stale spec) |
| E-6 | directory in owns | §2.4 | a wide directory is named, never silently skipped |
| E-7 | no reader at all | header `readers: ok -- ... 0 readers` | quiet on success (the owner's word 16.11, the FG7-49 finding) |
| E-8 | a path with spaces or Cyrillic | searched as a fixed string; printed as is (gitcmd sets `core.quotepath=false`, premise P8) | the printed path is the path git holds |
| E-9 | a file name starting with `-` | every pattern passed after `-e`, every path after `--` | a CLI argument never becomes a git option |
| E-10 | a stem shared by many files (`run`, `config`) | stems under 4 chars skipped; the cap of §2.4 | a flood never hides the overflow line |
| E-11 | binary files in scope | `-I` skips them | — |
| E-12 | the same reader names two owned paths | one line, names joined | one line per reader file |
| E-13 | `--base` names a branch other than origin/main | searched as given, header names it | the header always says what was searched |
| E-14 | `slow_tests.json` absent or malformed at the base | `slow: unknown` once in the header | as E-3 |

**Error direction (rule 1, a function reused in a more consequential role):** C1 is advice that feeds a NOTE and a
critic duty, not a gate. It may err toward OVER-reporting (a tool listed as a test, a comment mentioning a stem); it
must not err toward UNDER-reporting a literal mention in scope. Adversarial inputs that must stay on the safe side:
E-2 (unresolved base), E-3/E-14 (absent registry), a reader only in an untracked worktree copy (not listed — correct,
it is not on the base), a reader in a quarantined file (listed with its status, never dropped), a capped list (the
overflow line printed). The reused `_blob_sections` errs toward "empty sections" on a git error (unsafe for this
role) — hence E-2's order: resolve first.

### 2.6 What the tool never does

Fetches, writes, judges sufficiency ("this spec is complete"), refuses a dispatch, or calls its index a "radius"
(P27's blast-radius word: readers are evidence the roles read).

---

## §3 Wiring

### 3.1 `dispatch_new.py`

On success (after `decision.code == 0` and the cut is not degraded, premise P1 lines 140-150), and only when the
dispatch has owned paths, `dispatch_new` calls `owns_readers.report(owns, given, names)` and appends to stdout ONE
blank line and the rendered block. Refused dispatches still print nothing on stdout (existing invariant,
`test_dispatch_new.py:84-85`, premise P3).

- The tool raising anything → the headers are still printed, followed by the blank line and `readers: unknown --
  <ExcType>: <first line>`; exit stays 0. Invariant: a failing helper never blocks or hides a dispatch, and never
  prints `ok`.
- **Invariant of position (rule 11 (ii))**: the block never enters any manifest section's extent. It sits AFTER the
  last header line, behind a blank line (extents end at the first blank line, `dispatch_manifest.section_extent`,
  premise P2 lines 613-621); its lines never start with a manifest key or an id key after the `- ` bullet (the
  kinds `outside quarantined slow data absent exists unsearched` collide with none of `KEY_GROUPS`, `task`, `node`,
  `feature`, `manifest-skip`, premise P2 lines 84-93, 750); it carries no numbered line (`designer_threshold` counts
  them, P2 lines 859-871) and no absolute path. So `check`, `owned_paths`, `given_paths`, `header_ids` and the designer
  count are identical with and without the block — held by the existing round-trip test
  `test_printed_text_passes_check_and_ids_read_back` (premise P3) once a CASES row carries a block.
- `dispatch_gate.given_path_warn` reads paths on ANY line of a builder dispatch outside the checked sections
  (premise P15, `find_missing_given_paths` "any line"). A reader path absent from the WORKING tree but present on the
  base (a stale root checkout) would draw a GIVEN-PATH WARN. Accepted as is: that WARN is true (the launching
  checkout lacks the file). No change to dispatch_gate.
- New optional `--names` passthrough (fork F-2).
- Critic/designer/scout dispatches without owns: no block (nothing to search).

### 3.2 `dispatch_manifest.py` — a NOTE first, a refusal never in this spec

In `check_cut`, for a checked (builder or writing) dispatch that passes: if no unquoted line matches
`^readers:[ \t]*(ok|unknown|\d+ to act on)\b`, append to the notes exactly:

`READERS NOTE: this writing dispatch carries no readers: line -- run python -B tools/owns_readers.py --paths <owns>
(dispatch_new.py prints it) and keep its block, or write 'readers: unknown -- <reason>' when it cannot run.`

- Not a `KEY_GROUPS` item (fork F-5): adding one changes `ITEMS`, the INCOMPLETE and UNCHECKED texts and the
  manifest-skip item list (premise P2 lines 84-96, 137-154) — that is the promotion step, taken on evidence.
- Why the door is a hand-typed `readers: unknown -- <reason>` and not `manifest-skip: readers -- ...`:
  `manifest-skip:` accepts only `ITEMS` names, and an unknown item REFUSES the whole dispatch (P2 `_parse_skip_line`,
  lines 257-275). The hand-typed line matches the regex above and counts as an informed pass (FR-4). Small choice S-4.
- A degraded cut: no note (the UNCHECKED note already says nothing was checked).
- Order: after FG7-49 (it owns `tools/dispatch_manifest.py`, batch-7 line 72; status there reads «ожидает», while
  the brief says it is being edited now — noticed contradiction, §N).

Promotion rule (rule 10 (d)): the note becomes a refusal only on log evidence — two `failure_class: spec` rejects of
class a1/e on dispatches that carried no `readers:` line after the note shipped — and as a new spec node.

### 3.3 Who reads the block

- **builder**: keeps every `outside` reader green or names it in the report as "changes needed outside owns: <path>"
  and STOPS (a return, not an edit outside owns); never writes into a `quarantined` file; a `slow` owned test is
  named "judged by the batch canon" (builder-rules 7b). The line for this goes into `plans/builder-rules.md` — Lead
  edit L5 (the builders' standing rules file; not in this draft's given).
- **critic (diff gate)**: reads the block as the list for question 3 (seams) instead of grepping; a diff that
  breaks an `outside` reader without naming it is a finding.
- **critic (plan gate)**: §4.1.
- **designer**: §4.2.

---

## §4 The rule texts

### 4.1 The plan-gate question (home: fork F-6; recommended: a new section of `docs/tasks/critic-diff-brief.md`)

Text, to be added after item 12 as its own section:

```
## The plan gate (critic on a plan or on a dispatch draft; CLAUDE.md rule 3)

13. **FACTS AND EDGES** (evidence: t-896, 65 `failure_class: spec` rejects of 11-16.11.2026 -- 42 found by the code
    critic, 4 by the plan critic). Each sub-question gets its own verdict line.
    (a) EDGES: for every limit, empty or absent input, pair of the spec's own requirements, and artifact the change
    brings into existence (both worlds) -- is the behaviour stated, with the invariant it protects (CLAUDE.md
    rule 11)? A silent one is a finding named by the requirement that creates it.
    (b) MEANING: restate in one line what each changed field, gate or refusal means after the change; a restatement
    that contradicts another section or the spec's own example is a finding.
    (c) PREMISES: every statement about existing code, files or data carries a premise -- command + output, or
    file:line + quote. A statement without one is a finding; you do not supply it. Re-run ONE or TWO premises the
    plan rests on most (a signature, a flag, a field); one that does not reproduce blocks.
    (d) READERS: the plan carries the block of `python -B tools/owns_readers.py --paths <files it touches>` (or you
    run it) and gives every listed `outside`, `quarantined`, `slow`, `data` and `absent` line its answer: unchanged,
    changes in stream X, or a case moved to a keep file. A listed line with no answer is a finding. Do not re-grep
    what the tool lists; its KNOWN MISSES (docstring) are yours to judge.
```

Why (c) asks for one or two spot-runs and not all: CLAUDE.md rule 3 already says the plan review "checks the plan's
facts by trail"; the brief bounds the cost ("it does NOT re-run all premises"). (a) adds no new duty — it makes the
rule 11 edges a plan-gate verdict line; the text points, it does not copy.

Pointer in the critic role file (fork F-6): one line as rule 21 of `.claude/agents/critic.md`:

```
21. On a plan gate, the facts-and-edges question with its own verdict lines: docs/tasks/critic-diff-brief.md item 13.
```

Cost of touching `critic.md`: its rule 10 requires the critic exam in `PROCESS/CRITIC_EXAM.md` before the commit
(premise P16), and that file does not exist in this repo (PROCESS/README.md:22 "generated at onboarding; not present";
§N). Fork F-6 states the options.

### 4.2 The designer line (home: `.claude/agents/designer.md`, appended to rule 3)

```
   The readers list is the block of `python -B tools/owns_readers.py --paths <touched files> [--names <changed
   names>]`: you have no shell, so the Lead attaches it to the brief and the plan critic re-runs it on your
   touched-file list; quote the block and give every line its answer. A hand grep is owed only for what its KNOWN
   MISSES name.
```

The designer's `tools:` line is `Read, Glob, Grep, Write` (premise P17) — it cannot run the tool. That is why the
line routes the run to the Lead (brief) and the plan critic (who has `Bash`, premise P18). Fork F-8 covers the
alternative (give the designer Bash).

---

## §5 Tests (`docs/TESTING.md`: one parameterised test per behaviour, a world built once per file)

Witness scope: forge paths have no `scenario_walk.py --witness-for` row; the DoD names the test files that judge the
paths (CLAUDE.md rule 4).

**T1 — the tool's table** (home: fork F-9; recommended `tools/test_owns_readers.py`). ONE temporary git repo per
file: a tiny tree with a package-like `ai-packages/qa-factory/scripts/tests/` (a `test-layers.json` with one keep
and one quarantine row, a `slow_tests.json` with one slow file), `tools/`, one JSON carrier; committed; ref
`refs/remotes/origin/main` set by `git update-ref`; then one uncommitted file and one untracked worktree-like copy.
One parametrized test `test_owns_readers_table`, ids naming the case:

| id | input | expected |
|---|---|---|
| quiet | owned module + its only test both owned | exactly one line, `readers: ok -- ... all inside owns` |
| outside-test | owned module; its test not owned | `- outside: <test> (test) names <module>` |
| outside-code | another tool imports the owned module | `- outside: ... (code)` |
| data-carrier | a JSON names the owned file | `- data: ...` |
| quarantined-owned | owned test in quarantine | `- quarantined: ... (owned)` |
| quarantined-reader | reader in quarantine | listed with `(quarantined ... do not edit)`, not as `outside` |
| slow-owned | owned test over the threshold | `- slow: ...` |
| absent-given | given file only in the working tree | `- absent: ... (given)` |
| new-exists | owned `(new)` on the base | `- exists: ...` |
| new-absent | owned `(new)` not on the base | no line for it |
| untracked-copy | reader only in an untracked copy dir | not listed |
| base-missing | `--base origin/nope` | Example C line; no `ok`, no "not quarantined" |
| layers-absent | base without `test-layers.json` | `quarantine: unknown` in the header |
| outside-repo | `C:/elsewhere/x.py` | `- unsearched: ... outside the repo` |
| dir-small / dir-wide | a directory under / over 40 files | expanded / one `unsearched` line |
| cap | 13 readers of one file | 12 lines + `unsearched: 1 more ... --all`; `--all` lifts it |
| short-stem | owned `s0.md`, a file saying "s0" | not a reader unless it names `s0.md` |
| space-cyrillic | owned `my dir/ф.py` named by a test | found |
| dash-name | owned `-x.py` | searched, no git option error |
| empty-paths | `--paths` with a blank item only | exit 2, `OWNS_READERS REFUSED` |
| names-absent (if F-4 = a) | `--names nosuch` | `- absent: name nosuch ...` |

Outside-input battery (rule 11): magnitude (cap, dir-wide, PATH_CAP), encoding (space-cyrillic), broken/empty
(empty-paths, base-missing, layers-absent), injection (dash-name). Time: under 10 s, one world per file.

**T2 — the dispatch junction**, rows in the existing table of `tools/test_dispatch_new.py` (premise P3):
`readers-block` (BASE with a real owned tools file: stdout holds a blank line then `readers:`; the round-trip test
`test_printed_text_passes_check_and_ids_read_back` runs on it unchanged), `readers-tool-raises` (monkeypatch
`owns_readers.report` to raise: headers printed, `readers: unknown -- ...`, exit 0), and the existing refusal rows
keep `out == ""`. The test runs on the real repo with base `origin/main`; on a clone without that ref the row
expects the `unknown` form — the assertion is on `readers: ` being present and the round trip, not on its findings.

**T3 — the note**, rows in `tools/test_dispatch_manifest.py`: builder dispatch without `readers:` → `READERS NOTE`
in the note and exit 0; with `readers: ok ...` / `readers: unknown -- x` / `readers: 2 to act on ...` → no note; a
`readers:` line inside a fence → the note (quoted text never counts); a critic dispatch without owns → no note.

---

## §6 Phases, streams, owns, Lead edits

Streams (disjoint files; S2 waits for FG7-49):

**S1 — builder: the tool and its door**
```
owns:
C:/QAFactory/forge-repo/tools/owns_readers.py (new)
C:/QAFactory/forge-repo/tools/owns_readers.json (new)
C:/QAFactory/forge-repo/tools/test_owns_readers.py (new)
C:/QAFactory/forge-repo/tools/dispatch_new.py
C:/QAFactory/forge-repo/tools/test_dispatch_new.py
```
given: this spec; `tools/gitcmd.py`; `tools/test_quarantine.py` (`_blob_sections`); `tools/dispatch_manifest.py`;
`docs/TESTING.md`; `plans/builder-rules.md`.
non-goals: no change to dispatch_manifest.py, dispatch_gate.py, test_quarantine.py, any package file; no fetch.
edges: §2.5 E-1..E-14, §3.1 invariants.
DoD: `python -m pytest tools/test_owns_readers.py tools/test_dispatch_new.py -q` green; one measured run
`python -B tools/owns_readers.py --paths tools/dispatch_manifest.py tools/dispatch_gate.py ai-packages/qa-factory/scripts/selftest.py`
with its output and wall time in the report; the docstring carries KNOWN MISSES 1-6.
(If F-9 goes to option b, `tools/test_owns_readers.py` drops from owns and T1 goes as rows of
`tools/test_dispatch_new.py`.)

**S2 — builder, after FG7-49 is merged: the note**
```
owns:
C:/QAFactory/forge-repo/tools/dispatch_manifest.py
C:/QAFactory/forge-repo/tools/test_dispatch_manifest.py
```
DoD: `python -m pytest tools/test_dispatch_manifest.py tools/test_dispatch_new.py tools/test_dispatch_gate.py -q`
(test_dispatch_gate.py because the note travels through `decide_full`). Before launch the Lead runs S1's tool on
these owns and puts its block into the dispatch — the first live use.

**Lead edits** (one commit with the mechanism block of CLAUDE.md rule 10 — axes enumerated for EVERY axis of
`docs/SIBLING_MAP.md`; I did not read the map; the axes I know this touches: 13 (the one cut of a dispatch text,
named in dispatch_manifest's docstring), 18 (in-tree ratchets — the tool reads them), 31 (one owner per role
aspect — the pointer test), 34 (one road)):
- L1 `docs/tasks/critic-diff-brief.md` — the section of §4.1 (if F-6 = a or b).
- L2 `.claude/agents/critic.md` — rule 21 (if F-6 = b) + the exam question.
- L3 `.claude/agents/designer.md` — the §4.2 line.
- L4 `tools/tests/test_role_carriers_one_owner.py` — a POINTERS row `(".claude/agents/critic.md",
  "docs/tasks/critic-diff-brief.md item 13", BRIEF, "13. **FACTS AND EDGES**")` (if F-6 = b; the file pins every
  critic.md → brief pointer, premise P19).
- L5 `plans/builder-rules.md` — the builder's duty of §3.3.
- L6 CLAUDE.md rule 11 checklist point (5) freshness: one clause "for a writing dispatch: the `readers:` block of
  tools/owns_readers.py" — keeps every `install_parity_anchors.json` anchor of CLAUDE.md (premise P20).
- L7 `PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md` — the detector of rule 10 (c): re-run the t-896 count (class a1/e
  rejects per writing dispatch, and how many of their dispatches carried a `readers:` line) every calibration.

Rule 10's four questions, short: (a) cost — one tool run per writing dispatch (seconds, estimate), 1-15 block lines
per dispatch, the builder's stop on an outside reader, one or two premise re-runs per plan critic; (b) axes — the
commit block above; (c) detector — L7; (d) on the path — `dispatch_new.py` prints the block, the launch hook's NOTE
(C3) shows its absence; the plan-gate question rests on discipline with L7 as its detector.

### 6.1 Readers of every touched file (designer rule 3)

Grep scope `tools/`, `.githooks/`, `.claude/` excluding `.claude/worktrees/` (the Grep tool's glob exclusion did not
take effect for worktrees in my run, so worktree hits were discarded by hand). Positive control for `.githooks/`:
`mechanism_gate` → `.githooks/commit-msg:2`.

| Touched file | Command (Grep tool) | Hits (outside worktrees) | Reader → status |
|---|---|---|---|
| `tools/dispatch_new.py` | `dispatch_new` over tools/ | 2 files (dispatch_new.py 3, test_dispatch_new.py 7) | test_dispatch_new.py → changes in S1 |
| | over .claude/ | `.claude/skills/next-task/SKILL.md:39` | unchanged (says "lines from dispatch_new.py"; still true) |
| | over .githooks/ | 0 (control above) | — |
| `tools/owns_readers.py`, `.json` (new) | `owns_readers` over tools/ (-i) | 0 | dispatch_new.py → S1 |
| `tools/dispatch_manifest.py` | not grepped by me in full; known readers by its docstring (premise P2 lines 14-29): dispatch_gate.py, owns_gate.py, handoff_gate.py, dispatch_new.py, the dispatch-record hook, agent_budget.py (HANDOFF_DIRS) | — | all unchanged (the note is additive; `check`'s 3-tuple keeps its shape); the full list is S1's tool output, run by the Lead before S2 launches — a residual of this draft, named |
| `docs/tasks/critic-diff-brief.md` | `critic-diff-brief` over tools/ | 3 files: install_parity_anchors.json 1, tests/test_role_carriers_one_owner.py 7, test_handoff_rule_anchors.py 1 | anchors of existing items unchanged (append only); test_role_carriers_one_owner.py → L4 |
| | over .claude/agents | critic.md 4 | → L2 |
| `.claude/agents/critic.md` | `critic\.md` over tools/ *.py,*.json | install_parity_anchors.json:139-140 (anchors rules 1-17), test_role_carriers_one_owner.py, test_handoff_rule_anchors.py:33, dispatch_gate.py:65 (comment), critic_verdict.schema.json:5 (description text) | all unchanged (rule 21 appended; no anchor removed) |
| `.claude/agents/designer.md` | `designer\.md` over tools/ *.py,*.json | install_parity_anchors.json:168-169, test_role_carriers_one_owner.py:38/64-65, test_handoff_rule_anchors.py:36, journal_validator.py:162/349 (comments), mechanism_gate.py:668 (comment), test_journal_validator.py:801 (comment) | unchanged (a line appended inside rule 3; its first line stays) |
| `tools/test_quarantine.py` (imported, not changed) | `_blob_sections` over tools/ | test_quarantine.py 3, test_test_quarantine.py 2 (monkeypatches it) | unchanged; a rename of `_blob_sections` would now break owns_readers — S1's docstring names the import |
| `ai-packages/.../test-layers.json`, `slow_tests.json` (read only) | — | — | unchanged |

---

## F. Forks (each with options and a recommendation)

- **F-1 Search base.** (a) `origin/main` tree via `git grep <ref>` [recommended: excludes worktree copies and other
  sessions' uncommitted files; matches the builder's base "от origin/main"]; (b) the working tree (sees an unpushed
  local change, but also 67 worktree copies and a possibly stale root checkout); (c) both, with a diff. Cost of (a):
  an unpushed dependency is reported `absent` — which is the line-541 class, i.e. the right answer.
- **F-2 `--names`.** (a) optional `--names` on the tool and on `dispatch_new` [recommended — designer rule 3 already
  asks for "the file's name and its changed names"]; (b) search every top-level name the owned file defines (very
  noisy: `main`, `run`); (c) file names only.
- **F-3 Data carriers.** (a) scope globs, no list [recommended: a new ratchet is covered without an edit]; (b) an
  explicit carrier list (precise, but a second list next to critic-diff-brief item 9 and
  `source-split-carriers.json` — one road says converge first).
- **F-4 Name presence on the base** (widening the brief's (iv) from paths to names): (a) for every `--names` item
  with zero hits on the base, print `- absent: name <n> (named, not found on <sha>)` [recommended: replays 541 and
  partly 1972; costs one more -e per name in the same call]; (b) paths only, as the brief says.
- **F-5 Note mechanics.** (a) a separate presence regex, not a section [recommended for the note phase]; (b) a
  `readers` KEY_GROUP in note mode now (changes ITEMS and three message texts and their pinning tests).
- **F-6 Home of the plan-gate rule.** (a) new section in `docs/tasks/critic-diff-brief.md` only (critic.md rule 19
  already sends the critic to item 12 "on a plan gate" — but with no pointer to item 13 a plan critic may never open
  it); (b) (a) + critic.md rule 21 pointer + the L4 pointer row [recommended]; cost: critic.md rule 10's exam, whose
  carrier `PROCESS/CRITIC_EXAM.md` is absent — the Lead decides whether the exam is run from an inline role text
  (rule 10 allows "deliver the role text inline, noting the deviation") or recorded as not runnable; (c) a new file
  `docs/tasks/critic-plan-brief.md` + pointer (cleanest by title; one more carrier and one more pointer row).
- **F-7 slow_tests.json reader.** (a) parse it in the tool at the base [recommended; a named second reader]; (b) add
  a revision reader next to `_blob_sections` in test_quarantine.py (a change in another owner's file).
- **F-8 The designer and the shell.** (a) the Lead attaches the block to the brief; the plan critic re-runs it on the
  designer's touched list [recommended — P14/AR-11 analog: tools only as needed; the designer's Write is
  hook-limited]; (b) give the designer `Bash` (it could run the tool itself; widens a role whose hook regime is built
  for Write only).
- **F-9 Test file.** (a) new `tools/test_owns_readers.py` [recommended]: `docs/TESTING.md` «Бюджет / Файлы» allows
  a new forge tool its own test file only for the OFFLOAD spec (the owner's word 14.11.2026); this tool is the same
  class, so the Lead asks the owner whether the exception covers new forge tools in general; (b) without that word:
  T1 as a second table inside `tools/test_dispatch_new.py`, through the tool's Python API (legal now, awkward home).
- **F-10 Cap values.** 12 readers per path, 40 files per directory: my guesses from the 56-file `selftest` count;
  the Lead may set others.

## S. Small choices I closed

- S-1 Repo-relative forward-slash paths in the block (keeps the block out of `owned_paths` and absolute-path readers).
- S-2 Scope globs and caps live in `tools/owns_readers.json` (FR-13 analog: closed variety in data).
- S-3 Stems under 4 characters are searched by file name only.
- S-4 Until promotion, the note's door is a hand-typed `readers: unknown -- <reason>`, because `manifest-skip:`
  refuses an unknown item name (premise P2 lines 257-275).
- S-5 `dispatch_new` imports the tool (no subprocess); the tool reaches git only through `gitcmd.git`.
- S-6 No fetch; the header prints the searched sha.

## R. Replay — would PART 1's output have shown the fact? (journal notes + files as they are today)

| Line | Fact missed | Shown? | Why |
|---|---|---|---|
| 1117 (t-442) | frozen dict in test_walk_plan_fields pins `qa-retro-analyst 14075` after role-load raised | **probably no** | the pin is a VALUE keyed by role name; today's file names `role-load.json` only in a comment (`test_walk_plan_fields.py:253`), and the pin itself is gone (Grep `qa-retro-analyst\|14075\|14213` → 0; control `role-load` → line 253). With F-2 `--names qa-retro-analyst` it would have been found — KNOWN MISS 3 |
| 1181 (t-462) | analyst ratchet red outside owns | likely yes | `references/role-load.json` is keyed by role name = stem of the role file (`"qa-retro-analyst": 15826`, role-load.json:22) → a `data` line; I could not confirm which file was owned |
| 384 (t-133), 397 (t-134) | node tests written into quarantined files | **yes** | (ii): an owned/named test in `quarantine` gets its own line |
| 1060 (t-420) | DoD sent rows to a quarantined file | **yes** | same; the file was named in the DoD/owns |
| 1115 (t-439) | `test_import_test_receipt.py` edited while quarantined | **yes** | it is in quarantine (test-layers.json:8565, inside the section that starts at :7174); as a reader of the owned script it prints `(quarantined ... do not edit)` |
| 294 (t-113) | 99 reader-test fixtures lack siblings | **yes, as tests** | the tests that load those fixtures import `dispatch_manifest` → `outside` lines; the fixtures themselves (dispatch texts) do not name the module |
| 307 (t-113 #2) | three more fixture dispatches outside the DoD | partial | same reason; the fixture files are not readers by name |
| 829 (t-325) | selftest imports hooklib; breaks test_selftest_shard, _slow_tests | partial | both name `selftest` (in the 56-file list) → listed, but under the 12 cap they may land in the overflow; the real cause (the rule at selftest.py:93) is a2 — PART 2 (c) |
| 1395 (t-559) | test_conductor_doors.py red outside owns | likely yes | it names `s0_criteria`/`s0.md`/`driver.md` (2 hits) — listed if one of those was owned |
| 541 (t-199) | `require_project_at` only on unmerged batch-1 | no; **yes with F-4** | a FUNCTION, not a path: (iv) misses it; F-4 prints "name not found on origin/main" |
| 417 (t-148) | `value()` has no element argument | no | a signature (a2); PART 2 (c) |
| 551 (t-202) | receipt has no install signature | no | a data field's content (a2); PART 2 (c) |
| 1972 (t-803) | `--part exits:<group>` does not exist | partial with F-4 | `--names exits` reports zero hits only if the string is absent everywhere |
| 2172 (t-885) | 12 red tools tests after the landing | partial | the source pin on journal_echo and the hygiene `run_allowed` test name their tools → yes; the Linux exec bit → no (class c) |

Firm answers: yes 5 (384, 397, 1060, 1115, 294) plus 1181 likely; no 4 (1117, 417, 551, and 541 without F-4). That
agrees with the brief: PART 1 closes the quarantine and reader sub-classes, and PART 2 (c) carries the a2 share.

## N. Noticed contradictions and analogs (not widened)

1. The brief names `tools/ratchet-files.json` as a carrier: it does not exist (Glob `tools/*.json` lists 12 files,
   none of that name; `**/ratchet-files*` → none; positive control `**/dup-baseline*` → found).
2. The brief says FG7-49 is "being edited now"; `plans/piles/forge/batch-7-vhodyashchie-4.md:72` shows «ожидает».
3. `.claude/agents/critic.md` rule 10 requires `PROCESS/CRITIC_EXAM.md`; the file is absent (Glob `**/CRITIC_EXAM*.md`
   → none; control `**/WEEKLY_CALIBRATION_PROTOCOL*.md` → found; `PROCESS/README.md:22` says "not present").
4. `test-layers.json` note (line 3) says "Read only by scripts/selftest.py test_layers()", while
   `tools/test_quarantine.py::_blob_sections` (line 208) reads it at a revision — an existing second reader; this
   spec reuses it rather than adding a third.
5. Analog: `scenario_walk.py --witness-for` (lines 887-922) already maps a changed package path to keep rows and
   scenario tests, but never mentions quarantined files; C1 does not replace it (the DoD still names it) — a
   possible later convergence (one "who judges this path" reader), not in this spec.
6. FG7-53 ("owns judged at worker stop", batch 7) works on the same owns lists; no file overlap with S1/S2 is visible
   from its commit subject, but the Lead should check its row before launch.
7. The `.claude/` grep of designer rule 3 drowns in `.claude/worktrees/` copies (97 files for `dispatch_new`); rule 3's
   own grep would benefit from the same base-tree search.

## T. Reading trail (premises)

- P1 `tools/dispatch_new.py` read whole: docstring 1-17 ("Pure output: stdout only", "`<abs path> (new)`"); success
  path 140-151; `_path` 69-74.
- P2 `tools/dispatch_manifest.py` read whole: KEY_GROUPS 84-93; ITEMS 94; texts 137-163; PATH_CAP 189; section_cut
  319-374; section_extent 613-621; `_parse_skip_line` 257-275; `_IDS_HEADER_RE` 750; designer_threshold 859-871;
  check_cut 905-970.
- P3 `tools/test_dispatch_new.py` read 1-119: CASES 42-73; refusal prints nothing 84-85; round trip 99-118.
- P4 `.claude/agents/critic.md` read whole (rules 10, 12, 16-20). P5 `docs/TESTING.md` read whole («Бюджет / Файлы»).
- P6 `tools/test_quarantine.py:208-217` `_blob_sections`: `rc, txt = _git(root, "show", f"{rev}:{LAYERS_REL}")`;
  `if rc: return {"keep": {}, "quarantine": {}, ...}` — any git error reads as empty sections.
- P7 `ai-packages/qa-factory/scripts/slow_tests.json:1-25` (`thresholds.slow_over_s: 10`, `files`); selftest has
  `test_layers()` (selftest.py:645-664) but no slow reader at a revision found (Grep `SLOW_TESTS\b` over
  scripts/*.py → 4 prose/test hits, no definition).
- P8 `tools/gitcmd.py:1-3` "The one git runner of the tools"; `git()` at :38-39 runs `git [-C root] -c
  core.quotepath=false args...`.
- P9 Glob `**/dup-baseline*` → 68 paths, 67 under `.claude/worktrees/`.
- P10 Glob `tools/test_*.py` lists `tools/test_quarantine.py`, `tools/test_split.py` (tools) beside their tests.
- P11 `scenario_walk.py:887-922` `witness_for` (keep `covers` + scenario import closure).
- P12 `tools/source-split-carriers.json:3,14-31` ("`carriers` are the registries keyed by a file name").
- P13 `references/role-load.json:22,36` `"qa-retro-analyst": 15826 / 14477`.
- P14 Grep `selftest` over `scripts/tests` `test_*.py` → 56 files.
- P15 `tools/dispatch_gate.py:932-935` `find_missing_given_paths` "The paths of the prompt (any line)"; 956-961.
- P16 critic.md:58-63 (rule 10). P17 designer.md:5 `tools: Read, Glob, Grep, Write`. P18 critic.md:5 `... Write, Bash`.
- P19 `tools/tests/test_role_carriers_one_owner.py:53-68` POINTERS (critic.md → brief items 6-7, «The two layers», 12).
- P20 `tools/install_parity_anchors.json:1-40,137-179` (anchors of CLAUDE.md, critic.md rules 1-17, designer.md).
- Journal lines read: 294, 307, 384, 397, 417, 453, 541, 551, 829, 863, 1009, 1060, 1115, 1117, 1181, 1395, 1972, 2172.
  Not read: 420, 1090 (cited by the brief; quarantine class, same as 384/397).
- Package carriers located: Glob for role-load, judgment-census, form-rounds, env-facts-baseline, driver-layers,
  told-ratchet, role-rules, slow_tests → all 8 found (paths in §2.3).
- test-layers.json read 1-60, 7115-7204 (sections keep :36, pin_holds :7120, cohorts :7126, quarantine :7174);
  Grep for test_conductor_doors/test_selftest_shard/test_onboarding_notes/test_import_test_receipt → :672, :3464,
  :5185, :8565.

needed beyond the manifest: the files in the trail other than the five given.

## Lead decisions on the forks (Lead, 17.11.2026) -- the plan critic reviews the spec WITH these

F-1 (a) `origin/main`; F-2 (a) optional `--names`; F-3 (a) scope globs; F-4 (a) name presence on the base; F-5 (a);
F-6 (b) brief section + critic.md pointer, the exam recorded as not runnable (no exam file is registered: CLAUDE.md
rule 1, row R1-a analog; the Lead notes the deviation in the commit); F-7 (a); F-8 (a) the Lead attaches the block, the
designer gets no shell; F-10 caps 12 and 40 stand until measured. F-9: asked of the owner (does the 14.11 exception for a
new forge tool's own test file cover new forge tools in general); until her word, option (b) -- T1 as a second table in
`tools/test_dispatch_new.py`.
