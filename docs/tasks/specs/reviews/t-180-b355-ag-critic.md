# B-355 nodes A and G: critic-of-code review (task t-184; path kept as dispatched, t-180)

Critic (Opus), 12.11.2026. One pass on one topic (rule 13-g). Spec: `docs/tasks/specs/t-155-b355-project-word-for-test-paths.md`
§2 items 1, 1b, 2, 3, 4, 13, §3, §4, §5, "Closed 12.11.2026". Diffs: node A `6c5a8a3..wip/b355-a` (224bca9 + d54eea8), node G
`e20c3a2..wip/b355-g` (8846868, 5c55aa8, 98f7b07).

## Verdicts

- **Node A: fit_with_fixes.** There is no blocker for the merge itself. Two findings change behaviour, and both sit in
  `recorded_names` and the `name` binding. No live caller passes a config to the `name` consumer yet: judge_run.py:212 and
  gate_preflight.py:896 call it bare (grep below). Even so, A-1 must be fixed before node D wires judge_run. The fix belongs in
  A's code, as A's fix round.
- **Node G: fit_with_fixes.** One finding is a must-fix: two leftover sentences still send the whole 1c answer to `test_locations`,
  and that contradicts the new per-area rule.

The decision belongs to the coordinator. These verdicts are input to acceptance, not acceptance itself.

## Findings, ranked

### A-1 (must, before node D): `recorded_names` picks the wrong literal folder, so a project or source folder becomes a test name
`ai-packages/qa-factory/scripts/test_locations.py`, `recorded_names`: the line `keep(prefix.rstrip("/").rsplit("/", 1)[-1])` (the
run.levels and project-carrier loop) and the `ctx.entries()` loop.

**Why.** For `run.levels` it keeps the last segment of the LITERAL PREFIX. Spec item 4 asks for "the LITERAL last folder segment
of a live folder carrier". When the pattern has a wildcard before its trailing `**`, the prefix is a different folder, or the
project root itself. For `name`, True means "skip this identifier" (judge_run.py:208-226). The spec's stated error direction is
"noise, never a skipped project folder name", and these outputs break it. Probes (real verdict, temp projects, scratchpad
`probe2.py` / `probe3.py`):
- `run.levels {"unit": "packages/*/checks/**"}` (app_root `../app`): names = `{'packages', 'legacy'}`. `name("packages")` is True,
  `name("checks")` is False. A quoted `packages.billing.Invoice` is no longer grepped.
- `run.levels {"unit": "**/checks/**"}`: names = `{'legacy', 'myproj'}`. The project's own folder name becomes a test name.
- `test_locations ["src/**"]` with `protected_app_paths ["src"]` (an entry that covers a whole root and opens nothing): names =
  `{'src'}`, so `name("src")` is True and every quoted `src/...` identifier is skipped.

**Fix.** Take the folder name from the value as written. Drop a trailing `**`. Keep the last segment only when it holds no
wildcard, and never fall back to the resolved prefix when the remainder is non-empty (`**/checks/**` gives `checks`). Skip
`test_locations` entries whose `covered` list is non-empty. Add rows to `part_recorded`: `name-R-mid-wildcard`,
`name-R-glob-first`, `name-R-whole-root-entry`.

### A-2 (should): the `name` consumer is bound through the checkout; Lead decision (3) says it is ignored
`test_files.py` `is_test_for` / `_bind`. `name` has no path, but `_bind` asks `recorded(word, path=checkout/segment)`. The answer
then depends on which checkout is passed. Probe (`probe.py` P1; `app_root ../app`, `tests_root qa`):
- `name("qa", word=W, checkout=app)` gives False.
- `name("qa", word=W, checkout=proj)` gives True.
- `name("qa", W)` gives True.

So "a word and a checkout ignores the checkout" is not what the code does. The False answer is the safe side (noise), so this is not
a safety defect. It is an inconsistency between two calls of one consumer.

**Fix.** In `is_test_for`, when `consumer == "name"` and `word` is given, judge with `cfg=word` and do no binding. The Lead decides
whether `checkout=None` keeps returning None for `name` (today's code), or judges by the word: spec item 4 has `name` read "any
area" anyway. Add one row, `name-R-checkout-ignored`.

### A-3 (minor): the World N twin of E16 was lost in decision (1)
`scripts/tests/test_test_locations.py:364`. The row was rewritten to World R. Afterwards no verdict row asserts that the World N
reason names `references/test-path-markers.json` (grep `test-path-markers.json" in` returns only :1022 `suggest` and :1343, which
is World R). K3 kept its World N twin (the `none` loop, :214-216); E16 did not.

**Fix.** Add one row with the same fixture minus `test_locations`. Markers are missing, and the reason should contain
`test-path-markers.json`.

### A-4 (minor): F-12 has no real-config World R row
`part_recorded` has no row for a helper inside a recorded `tests_root` / `roots.test` place. The probe shows the code is right:
`file_kind("qa/helpers.py")` is `production` and `qa/test_x.py` is `test` under `tests_root qa`. The F-12 rows at :76-94 use a
mocked verdict with no config, which is World N for `rec`.

**Fix.** Add the row `production-R-helper-in-recorded-place-kept`.

### A-5 (minor, wording): "AND" in the docstring table reads as an intersection
`test_files.py`, module docstring, `"name"` row: "with one unrecorded: that set AND the usual names". The code is a union.

**Fix.** Write "that set plus the usual names".

### G-1 (must): two sentences still send every 1c answer to `test_locations`, relative to app_root
- `skills/qa-onboarding/phases/p2-interview.md:135-136`: "The answer becomes `config.test_locations` (entries relative to
  `app_root` …)". The sentence before it now invites places "inside the application folders or elsewhere".
- `skills/qa-onboarding/phases/p4-generate.md:91-92`: "`test_locations` (topic 1c's answer, as given, relative to `app_root` …)".
  This file is G-owned, and spec §0 F-12 names p4:91.

**Why.** New 1c text at p2:122-125 says to record the answer "in the carrier of THAT area". A role that follows the later sentence
would write a test-repository place into `test_locations`. Relative to app_root it needs `..`, and `config-keys.json:317` says such
an entry "opens nothing". Spec item 2 rows (`["", "/abs", "../x"]` mean not recorded) agree. Result: the project area stays silently
unrecorded and the person's word is lost (AR-22, AR-24, FR-8).

**Fix.**
- p2:135: "The answer is recorded in the carrier of its area (above): a place inside the application code becomes
  `config.test_locations` (entries relative to `app_root` …)".
- p4:91-92: "`test_locations` (topic 1c's answer for the application code, relative to `app_root`; `[]` when none were named), and
  1c's answer for a test repository in `tests_root` / the profile's `roots.test` / `run.levels`".

### G-2 (minor): which carrier can hold a FILE shape, and how "always" meets "never re-asked"
`p2-interview.md:126-130`.
- The test-repository carriers `tests_root` and `roots.test` name folders only (`_live_carriers` gives them `rest None`). There, a
  file shape is possible only through `run.levels` (or `test_locations` in the application).
- "Asked ALWAYS" and "a recorded answer … is never re-asked" can be read against each other on a re-onboarding.

**Fix.** Add one clause: "a file shape goes into `test_locations` or a `run.levels` pattern; `tests_root` and `roots.test` name a
folder". Write "asked always when nothing is recorded for that area yet".

### G-3 (minor): the p4 heading and "covers" are not handed to the role
`p4-generate.md:365-369`. The heading still reads "Test locations inside the application code". The new sentence asks for
candidates "no recorded carrier of its area covers" but names no command for it (AR-8, FR-15).

**Fix.** Widen the heading. Point to `test_locations.py --root . --check --candidate "<p>" --json`, the form p2 already uses, as the
way to see whether a candidate is covered.

### G-note: p3 is outside spec §4's owns
p3-summary-gate.md is not in spec §4's owns for G. The dispatch lists it, and it is a correct same-artifact sibling: the summary
echoed the old "inside the application folders only". There is nothing to fix, but the Lead should note the owns amendment.

## Lead decisions (1)-(4)

1. **The three rows edited to World R: confirmed.** The fixtures carry `test_locations` with app_root `.` (the tie), so the area is
   recorded. Item 3's "existing rows stay green" contradicted item 3's own invariant ("in a recorded area no path becomes a test by
   the list"). The edits are correct. One cost remains: E16's World N coverage was dropped (A-3).
2. **The reading of `recorded_names`: corrected.**
   - The carrier set is right: `test_locations` entries whose effective segments end in `**`, plus `run.levels` with no remainder
     or one ending in `**`, plus `roots.test` / `tests_root`. This is the same folder-kind rule the verdict uses.
   - The area filter on project carriers is only a noise-side divergence. A tie or app-placed `roots.test "e2e-suite"` still
     recognises `e2e-suite/x.py` as a test in step 2b, yet `name("e2e-suite")` is False (probe2). I recommend dropping the filter
     for the NAME set and keeping it for `every`, but this is optional.
   - The SEGMENT taken is wrong (A-1): that is the correction.
   - Spec-level note for the Lead: O-2 now asks onboarding to record FILE shapes. A project recorded only by file shapes gets an
     empty name set and `every=True` (probe P3: `name("test_cart.py")` is False). judge_run will then grep test names: safe
     direction, more noise. Either accept and state it, or let file-shape carriers add their literal folder. The decision is the
     Lead's (queued below).
3. **`name` with a word and a checkout: corrected (A-2).** The checkout is not ignored. With a word and no checkout, the result is
   None when anything is recorded: confirmed (probe P1 `word unbound` gives None). That matches item 4, and for judge_run None
   means "grep it", the safe side.
4. **`recorded(path="")` returns `(False, [], "")`: confirmed.** It is safe (World N), it agrees with the verdict's "no path was
   given", and it is pinned (`test_test_locations.py` "an empty path names no area"). Suggestion: the docstring could say that
   `""` is not "any area".

## Standing questions

**Duplication and consistency (brief item 6).**
- Good: `_target` replaces the inline join in step 1. `_deepest_base` serves both step 4 and `area`. `_live_carriers` carries the
  ignore rules for both `_recognition` and `recorded` (AR-13 kept). `test_path_grants._is_test_specific` now calls
  `dir_marker` / `name_marker`.
- Found: `recorded_names` repeats the folder-kind expression of `_recognition` (`not rest or rest.endswith("**")` against
  `rest and not rest.endswith("**")`) and of `_config_match` (`segs[-1] == "**"`). Fold them into one `_folder_kind(rest)` helper
  in the A-1 fix round.
- Grep for marker lists outside the leaf (`dir_names|dir_suffixes|name_marker|dir_marker`, case-insensitive, `scripts/*.py` minus
  tests) returns test_files.py, test_locations.py, test_path_grants.py, plus `repo_map.UTIL_DIR_NAMES` and `selftest.SKIP_DIR_NAMES`.
  The last two are other classes and existed before. No new folder-name tuple was added: AR-1 kept.

**Code quality (brief item 7).**
- `_Ctx` is built twice per `_decide` call (verdict, then `recorded`). That is acceptable at this size.
- `str(path …).replace("\\", "/")` now appears three times in test_files.py. It is minor and follows an existing pattern.
- Otherwise the code reads cleanly and every new function is "never raises" with a pinned failure row.

**Judgment (q10/q11).**
- `area`, `recorded` and step 3b judge only data: presence of a carrier, path joins.
- Where tests live stays the person's word; onboarding (G) has the role propose and the person decide (AR-2, AR-7, AR-29 kept).
- F-12 (a) holds: `production` code is unchanged, `not v["test"]` keeps a file counted, and a name only narrows inside a place the
  record already names. Probes: `qa/helpers.py` is production, `helpers/x.test.ts` in the recorded project area is production.
- `test_judgment_census.py` is green (22/22). No new unit was required.

**One road (item 12, P31).** Every consumer reaches the same leaf with the same area rule. There is no language or project branch;
the only branches are by consumer and by error direction (F-12, the `name` union), and they are the same for everyone.

## Class-wide completeness (spec §5)

| sibling | status |
|---|---|
| Same-artifact sweep: `test_files` consumer table | applied: the docstring column was added (A-5 wording) |
| `test_path_grants` (axis 9) | applied |
| `test-layers.json` covers lines | applied; `test_probe_by_code.py` already covers `probe_by_code.py` (read) |
| readers of `test_body` / `name` and the diff sites | nodes B, C, D, F, I, H; not under review |
| onboarding p1/p2/p4 (G) | applied, except the p2:135 and p4:91 leftovers (G-1) |
| p3 summary | applied (outside spec owns, a correct sibling) |
| config-keys / template `test_locations` note | not covered; queued below (OF3-1 a owns) |

**AR-n.** AR-1, AR-3, AR-13, AR-23 and AR-28 are kept by the code (probed: World N is today's answer for absent / `{}` / junk
carriers; unreadable markers give a False verdict and never "test"). Node A's commit names only AR-2 and AR-29, while spec §1 names
more. This is minor and the gate passes.

## The witness

Control re-runs on the node A worktree match the witness rows exactly:
- test_test_files 152/152
- test_test_locations 505/505
- test_protected_test_path 378/378
- test_judgment_census 22/22 (an extra cheap check)

No inconsistency was seen between the witness and the diff. The negative control is plausible: the 3b-off failures (11 and 7) fall
on `part_recorded` rows.

## Queue (outside A and G, not part of the verdict)

- **Q1.** `references/config-keys.json:317` and `templates/config.json:8` (`test_locations` note, owned by OF3-1 a). The notes do
  not say that a non-empty list ends the usual-name fallback for the application area (B-355), and do not mention the
  test-repository carriers (AR-10).
- **Q2.** Spec note for the Lead: file-shape records (O-2) leave the `name` set empty (decision 2 above). Choose before node D.
- **Q3.** FR-33: G's prose is "closed by code, not proved". Its rows go to `live-runs` per PROJECT.md.

## Trail

- **Read:** spec t-155 in full; both diffs in full; `test_locations.py:240-365` and :583-592 (worktree); judge_run.py:196-230;
  p4-generate.md:86-96 (worktree G); `test-layers.json` `test_probe_by_code.py` covers; commit bodies (architecture / judgment);
  `tools/critic_verdict.schema.json`.
- **Greps:** `is_test_for\(\s*"name"|recorded_names|\.recorded\(|names_a_test\(` (-i, `scripts/*.py`): `name` callers are
  judge_run:212 and gate_preflight:896, both without a config. The positive control in the same shape found test_test_files.py:129.
  Marker-list grep as above. Onboarding grep `topic 1c|1c\b|inside the application (folders|code)` (-i, skills/references/agents).
- **Probes:** probe.py, probe2.py, probe3.py in the scratchpad, run with real `test_locations` / `test_files` on temp projects.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "class_completeness": "Spec 5 siblings for A and G applied (consumer docstring column, test_path_grants fold, covers lines, p1/p2/p3/p4) except G-1: p2-interview.md:135 and p4-generate.md:91 still route the whole 1c answer to test_locations; config-keys/template note queued (Q1, OF3-1 a owns). Diff sites B-J out of scope.",
  "fixes": [
    "A-1 test_locations.recorded_names: take the literal last folder segment of the value as written before a trailing ** (never the resolved prefix when a wildcard remainder exists); skip test_locations entries that cover a whole protected root; rows for packages/*/checks/**, **/checks/**, src/** whole-root",
    "A-2 test_files.is_test_for: the name consumer judges with cfg=word and no checkout binding (Lead decides the unbound None); one row",
    "A-3 test_test_locations.py: add the World N twin of E16 (markers missing, no test_locations, the reason names test-path-markers.json)",
    "A-4 part_recorded: add production-R-helper-in-recorded-place-kept (F-12 with a real config)",
    "A-5 test_files.py docstring: name row says that set plus the usual names, not AND",
    "G-1 p2-interview.md:135 and p4-generate.md:91-92: the 1c answer goes to the carrier of its area, test_locations only for the application code",
    "G-2 p2-interview.md 1c: say a file shape goes into test_locations or run.levels; asked always when nothing is recorded for that area yet",
    "G-3 p4-generate.md:365: widen the heading and name the --check --candidate command for covered"
  ],
  "trail": {
    "read": [
      "docs/tasks/specs/t-155-b355-project-word-for-test-paths.md",
      "git diff 6c5a8a3..wip/b355-a",
      "git diff e20c3a2..wip/b355-g",
      ".claude/worktrees/b355-a/ai-packages/qa-factory/scripts/test_locations.py:240-365,583-592",
      ".claude/worktrees/b355-a/ai-packages/qa-factory/scripts/judge_run.py:196-230",
      ".claude/worktrees/b355-g/ai-packages/qa-factory/skills/qa-onboarding/phases/p4-generate.md:86-96",
      ".claude/worktrees/b355-a/ai-packages/qa-factory/scripts/tests/test-layers.json (test_probe_by_code covers)",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/b355-a/ai-packages/qa-factory/scripts/tests/test_test_files.py", "result": "=== test_test_files: 152/152 ok ==="},
      {"command": "python -B .claude/worktrees/b355-a/ai-packages/qa-factory/scripts/tests/test_test_locations.py", "result": "=== test_test_locations: 505/505 ok ==="},
      {"command": "python -B .claude/worktrees/b355-a/ai-packages/qa-factory/scripts/tests/test_protected_test_path.py", "result": "=== test_protected_test_path: 378/378 ok ==="},
      {"command": "python -B .claude/worktrees/b355-a/ai-packages/qa-factory/scripts/tests/test_judgment_census.py", "result": "=== judgment_census: 22/22 ok ==="},
      {"command": "python -B scratchpad/probe3.py (run.levels **/checks/**; test_locations src/** whole root)", "result": "glob-first names {legacy, myproj}, name(myproj) True; whole-root names {src}, name(src) True"}
    ]
  }
}
```
