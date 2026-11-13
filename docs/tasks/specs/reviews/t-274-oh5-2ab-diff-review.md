# t-274: critic on the DIFF, topic OH5-2, Parts A and B (one pass, R13-g)

Reviewer: critic (Opus), 13.11.2026. Base `18a43b9`. Part A `refs/remotes/origin/wip/oh5-2a` (21be568 + fix 87b62fa).
Part B `refs/remotes/origin/wip/oh5-2b` (c58f295 + 4e17ade). Spec: `docs/tasks/specs/t-254-oh5-2-plugin-root-given.md` rev 2,
including the coordinator-decision paragraph and the 05:15 amendment. Read-only worktrees `.claude/worktrees/oh5-2a|oh5-2b`
are at the branch heads and clean.

**Verdict:** Part A is fit_with_fixes (4 fix-round items, none blocks the merge on correctness). Part B is fit_with_fixes
(1 item: attach the rest of the witness, plus the changelog fragment both parts share). Neither part has a blocking finding.
I found no defect in either product change. Every fix item is a test, witness or carrier gap. The coordinator decides
acceptance (rule 6).

## Answers to the dispatch's questions

**1. Survivor vs §3.1 / E1-E15. Answered: holds.** `runtime_paths.script_path`/`script_command` (A `runtime_paths.py:234-266`)
match §3.1.
- Default root is `package_root()`, and no `os.environ` read exists.
- Posix spelling: on nt, E2 backslash and E8 UNC give `//srv/share/...`. E7 non-ASCII is kept as is.
- E3a: a root holding `$`, a backtick or `"` gets single quotes. E3b: a root that also holds `'` gets the plain-text form.
- E4: the gap text matches the spec exactly. `must_exist=False` skips E4 and keeps the quoting rule (E3c row).
- All 11 sites go through it: `_config_door` :771-772 (`script_path` gate kept, so the missing form is never printed),
  `_section_door` :825, `big_read_check` :878, `handoff_write_check` :1089 and :1110, `artifact_rewrite_check` :1241,
  `plan_write_check` :1283, :1285, :1296, :1309, `_window_refusal` :1626.
- Argument tails stay after the returned text (N5). DoD (3) pins one E4 rendering (`test_refusal_registry.py` part_door_texts).
- E10, traced at every site: each import and call sits on the block path. That is the `_config_door` body past the
  config-path match, `_section_door` past a non-empty map, the `... if "Bash" in ways else ""` conditionals (evaluated only
  when true), and the block arguments of `handoff_write_check`/`_window_refusal`.
- E11: the finding and the 11 rewrites land in ONE commit (21be568). A24 keys are unchanged: `refusal_registry --check` rc=0.
- Grep check: `grep -ci claude_plugin_root` gives 0 on A `guard_pre_tool.py`; the positive control on A `hooks/hooks.json` gives 19.

**2. `_host_root_lines`. Answered: correct, scope as specced.**
- It walks every `ast.Constant` str of each SCANNED file. On Python 3.12.10 the literal parts of a JoinedStr are Constants
  that `ast.walk` visits, with true line numbers (PEP 701).
- E13 false positives: today there are 0. On the A tree, `stage_guard.py`, `inject_context.py` and `guard_pre_tool.py` give
  0 hits each. On conv/wave-5, which adds `native_context.py` to SCANNED, native_context and inject_context give 0 (control
  hooks.json 19).
- `refusal_registry.py` is not in SCANNED, so its own `HOST_ROOT_VARIABLE = "claude_plugin_root"` constant cannot self-flag.
- The concatenation miss is named in the docstring and pinned as a variant row. Implicit literal concatenation is joined by
  the parser, so it is flagged, which is the stronger side.
- No `*_problems` name, so it is not a census unit (judgment_census 22/22 in the witness).

**3. `SCRIPTS` at import vs `package_root` at call. Answered: no production divergence; one code-quality item (A4).**
- `package_root()` is `Path(__file__).resolve().parent.parent`, deterministic, so both are the same value in any process.
- After the change, `brief_pack.SCRIPTS` has NO production reader. `grep -n SCRIPTS brief_pack.py` gives only :72 and a
  comment at :1119.
- Only tests read it: `test_package_generation.py:472` and `test_brief_pack_roles.py:245-246` (both quarantined),
  `test_brief_pack_s5_plan.py:779`, and `test_refusal_registry.py:141`. All of them hold for every root: an E3a single-quoted
  card and the E3b plain-text form still contain the folder as a substring.
- Divergence arises only when a test patches `RP.package_root` and then reads `SCRIPTS`. M-6 does not read SCRIPTS. K6
  derives the root from SCRIPTS (`lambda: Path(SCRIPTS).parent`) and `FIXED_SCRIPTS` ends in `/scripts`, so the pinned bytes
  are identical. No caller passes `build(scripts=...)`.

**4. Part B join. Answered: non-vacuous; reads `host_adapter.role_has_bash`; Bash is never detected by regex.**
- `charter_card_join` (B `test_ahead_cards.py:166-191`) skips roles where `host_adapter.role_has_bash(role)` is False (axis 19).
- It extracts the `(on your card)` marker with `ON_CARD_RE`. That is the marker form DoD (3) defines, not a reading of the
  `tools:` line.
- It checks each name against `TOOLING`+`TOOLING_MANUAL`, and asserts the found set equals exactly the five pairs.
- Traced: the runner's `manual_capture.py` (`ui`, `http`) does not match (no marker before `)`). The strategist's "on your
  card" (:73) names no `.py`.
- The carrier scan (agents + slices, case-insensitive) gives 0 on B.

**5. Ratchets. Answered: lowered only; values equal the measure; no raise.** My run of
`python -B <B>/scripts/role_load.py --all --json`:

| role | process_tokens |
|---|---|
| scout | 13971 |
| strategist | 15392 |
| case-designer | 12079 |
| automator | 18685 |
| code-critic | 17593 |
| runner | 14417 |
| failure-analyst | 16322 |
| bug-reporter | 13914 |
| doc-scribe | 16943 |
| retro-analyst | 13198 |
| requirements-tester | 11280 |
| case-critic | 15929 |

- Each value equals its B row. The first 10 are the rows lowered from the base, matching the dispatch's list. The last two
  are unchanged; they have no slice, and the measure equals their old rows.
- `ratchet_tokens` is untouched. Part A raises no ratchet and adds no census row (AR-20).

**6. Merges. Answered: all mechanical and clean.** I ran `git merge-tree --write-tree` (no worktree touched); every pair
merges clean:
- A+B, A+origin/main, B+origin/main;
- A+conv/wave-5 and B+conv/wave-5.

A and B share no file, so the three-way result equals the pairwise ones.
- Overlap region, A vs wave-5/oh6-4 in `refusal_registry.py`: wave-5 edits the docstring (:30-35), `SCANNED` (:56) and
  REGISTRY entries (:339ff). A adds after `escalations()` (~:900) and in `findings()`. These are disjoint hunks.
- `judgment-census.json`: only wave-5 edits it.
- Semantic check after the merge: the new finding also scans `native_context.py`, which holds 0 hits. The merge stays green.
- My overlap scan of the A/B owns across every unmerged origin branch found only conv/wave-5 and wip/oh6-4
  (`refusal_registry.py`).

**7. Class completeness. Answered; see the map walk below.** OH5-2d and OH5-2e are known and not re-raised.

## Coordinator decisions judged

- **(i) Correct; the test meaning is preserved.**
  - The card head now reads `package_root`, so patching it is the only seam that reaches the card. The old seams
    (`brief_pack.SCRIPTS`, `G.PLUGIN_ROOT` for the door) became inert.
  - K6 negative control: the expectation `python "/<x*150>/scripts/<script>"` is the real layout (root = parent of
    scripts). It still fails if the card stops following the running copy.
  - M-6 world 1 and world 2 still prove both TEMPORAL worlds. `G.PLUGIN_ROOT` must stay patched because the guard reads
    role files through it (:1210/:1213).
  - Observation, not a finding: the K6 "path independence" loop (`for running in ...`) was inert before and is inert now.
    `build()` overwrites the pinned value, and `SCRIPTS` has no product reader.
- **(ii) Correct.** "`references/…`, `scripts/…`, the script paths on your card" still keeps project paths out of the
  installed-plugin frame (N3), and it avoids the raise E23 forbids. The 10 rows are verified above.

## Findings (fix round; none blocks the merge on correctness)

**A1 (Part A, test kills nothing): the K5 E5 row is vacuous.** At `test_runtime_paths.py` (k5, "E5" block), the row sets
`CLAUDE_PLUGIN_ROOT=C:/elsewhere` and then calls `RP.script_command("x.py", real)` with an EXPLICIT root. The env can never
reach it. Failure scenario: `script_command` changed to `root or os.environ.get("CLAUDE_PLUGIN_ROOT") or package_root()`.
The row still passes, because `real` is passed, and the defect E5 exists for ships. Fix: call with the default root,
`RP.script_command("runtime_paths.py")`, under the patched env, and assert it equals
`RP.script_command("runtime_paths.py", RP.package_root())` and does not contain `elsewhere`.

**A2 (Part A, TESTING.md «не пишется»: a source pin).** `test_refusal_registry.py` part_door_texts (:141-147) `ast.parse`s
`brief_pack.py` and counts `script_command('<script>', must_exist=...)` call nodes == 2. That pins the script's source, not
its behaviour: a refactor that keeps the behaviour goes red, and a third, hand-made card head added elsewhere stays green.
Fix: drop the AST count. Assert behaviour instead: patch `RP.package_root` to a root holding `$`, render
`brief_pack.command_card_lines(...)` (pure) and assert the head contains `RP.script_command('<script>', must_exist=False)`.
That is the single-quoted form, so E3c is proved through the card itself.

**A3 (Parts A and B, carrier): no `changelog.d/` fragment.** `plans/builder-rules.md` item 11 says the CHANGELOG entry is
a fragment `ai-packages/qa-factory/changelog.d/<pile>-<batch>-<slug>.md`. Neither branch has one, yet role-visible text
changed: guard doors now print absolute paths, and the charters and legend changed. Neither part's `owns:` listed
`changelog.d/`, so this is a dispatcher omission. Fix: one fragment per part (owns extended), or one shared fragment written
at integration.

**A4 (Part A, DUPLICATION/CONSISTENCY, fix before merge as minor):**
- (a) Inside `guard_pre_tool.py`, the same action has two spellings. Three sites (:771-772, :825, :878) do
  `import runtime_paths as RP; RP.script_command(...)` inline. The other eight call the new `_door_command` (:1117-1121),
  whose docstring says it exists for exactly that lazy-import purpose. Route :825 and :878 through `_door_command`.
  `_config_door` may keep `RP.script_path` for its gate.
- (b) `brief_pack.SCRIPTS` (:72) has no product reader now (Q3), but its comment block (:66-71) still says it is "what the
  role's Bash must use". Reword the comment: the survivor spells the card, and SCRIPTS is kept as the folder value for
  readers in tests.

**B1 (Part B, witness, rule 7): the attached mechanical layer covers 4 of the 22 files `--witness-for` prints.** My run of
the DoD's `scenario_walk.py --witness-for <B owns>` prints the files below; the layer attaches only test_role_load,
test_audit_rules, test_ahead_cards and test_charters (pytest).

```
test_ahead_cards test_audit_rules test_brief_pack test_bug_records test_charters_s5_s9 test_contract_slices
test_delivery_ownership test_first_look_wiring test_manual_capture test_project_decisions_change_request test_readiness
test_role_load test_scenario_{cart_1,local_1_0108,local_1_arm_b,walk,world} test_stage_joints test_story_run_monorepo
test_third_verdict test_validator_class test_walk_plan_fields
```

`contract_slices --check` stands in for test_contract_slices only partly. Risk is low: my targeted grep of non-quarantined
tests for the old legend cell or the old charter spellings found no pin; the only hits are in the quarantined
`test_brief_pack_roles.py`/`test_package_generation.py`. Fix: attach the builder's run of the remaining non-quarantined,
non-slow files (the slow `test_story_run_monorepo` goes to CI per PROJECT.md p.2), or the branch pipeline result.

## Standing questions

- **Fit to spec:** A DoD (1)-(5) and B DoD (1)-(5) are met, except the test quality items A1/A2 and the witness gap B1.
- **Builder's own decisions:** `_door_command` helper (fine, but see A4a); `script_path` swallowing `OSError`/`ValueError`
  to `None` (safe side: gap text, never a fabricated path); B's substring check `name in flat` (adequate for 5 distinct names).
- **Seams:** additive. `hooklib`, `stage_guard` and `inject_context` are untouched.
- **DUPLICATION AND CONSISTENCY:** A4a and A4b as above. I grepped `HERE.as_posix()|HERE.parent` over the scripts:
  - `handoff_check.py:2836` (spec's :2796, drifted) is queued to OH5-2d.
  - Reported analog, not in the queue: `brief_pack.py` reads the package root by hand at seven spots (:1121, :3326, :3582,
    :3600, :3766, :3881, :4273). The guard reads it through `hooklib.PLUGIN_ROOT` at eight spots (:564, :566, :733, :1210,
    :1213, :1923, :2507, :2618).
  - These are reference and agent paths, not script commands, and none prints the literal. It is still two readers of one
    fact (AR-13); M-6 had to patch both, which shows it.
  - Proposed node, for the coordinator's doc batch that opens OH5-2d: widen OH5-2d's row by "package-root readers converge
    on `runtime_paths.package_root`", owner = the coordinator of that batch.
- **CODE QUALITY:** no new function over 60 lines and no deep nesting (`script_command` is 19 lines). The dead production
  constant is A4b. Nothing else found.
- **Hygiene:** non-ASCII in the A test is spelled by escapes (FR-30). The legend's `…` was already there. The witness has
  selftest `--lang` 4/4.
- **IN-TREE RATCHETS:** 10 `process_ratchet_tokens` rows lowered (listed in Q5). No raise. No census row added.
- **ARCHITECTURE:** A's commit names AR-15 ("survivor added, axis queued to Lead (F7)"), AR-8, AR-13 and AR-29. B's commits
  name AR-8 and AR-20. AR-5 holds (hooks/*.json untouched, no host branch). AR-13 is partial by design; see the analog above.
- **JUDGMENT:** `_host_root_lines` is a token-presence shape check, owner data (`judgment: adds data check` line present). B
  adds no check and no `kind: craft` marker. No judgment moved into code.
- **ONE ROAD:** E3c makes the card and the door one spelling for every root, E3 roots included. No language, project or case
  branch was added. None found: I grepped the diff for host or language names (`codex|claude|python` in new branches); only
  the survivor's literal `python` spelling, the same for every host.

## Class completeness (SIBLING_MAP)

Class: a path a role needs is given, never an unexpanded host variable. Map walk:

| Axis | What it covers | State |
|---|---|---|
| 3 and 8 | where the package and the story live | do not host it; the new axis 37 is queued to the full Lead (F7, still open: the Lead commits it at merge) |
| 18 | ratchets | covered (Q5) |
| 19 | the `tools:` line reader | covered (`role_has_bash`) |
| 32 | census / one refusal-site scanner | `_host_root_lines` walks string constants, not refusal sites, so it is not a second `sites()` walk; no census unit |
| 34 | one road | E3c |
| 6 | measurers | Part C, outside this review |

Residuals OH5-2d/OH5-2e are known. Plan-review B2 (the carrier: findings files + batch-6 rows + README rows) is still owed by
the coordinator's doc batch at Part A acceptance. The quarantine reds of E22 (K9, P4, P5) are expected after B. The Lead
tells the owner in the same turn (F6); the B builder's list was not in what I was given.

## Trail

Read: spec t-254 (whole); plan review t-257 (whole); `docs/tasks/critic-diff-brief.md` (:8-100); `docs/SIBLING_MAP.md`
(axis list, axis 32-34); `tools/critic_verdict.schema.json`; both branch diffs (whole); A `guard_pre_tool.py` :755-830,
:1222-1300, PLUGIN_ROOT uses; A `brief_pack.py` SCRIPTS sites, :1112-1125; A `tests/test_brief_pack.py` :2164-2177,
:2255-2275; B `host_adapter.py:519-523`; conv/wave-5 diff of `refusal_registry.py` and `judgment-census.json`; commit
messages of the 4 commits; `plans/builder-rules.md` changelog lines.

Reruns (verbatim tails):
- A `test_runtime_paths.py`: `=== test_runtime_paths: 101/101 ok ===`
- A `test_refusal_registry.py`: `=== test_refusal_registry: 253/253 ok ===`
- A `refusal_registry.py --check`: `A24 refusal registry: no violations`, rc=0
- B `test_ahead_cards.py`: `=== test_ahead_cards: 245/245 ok ===`
- B `test_role_load.py`: `=== role_load (the one measure of a role's start load): 171/171 ok ===`
- B `role_load.py --all --json`: process_tokens equal every row (Q5)
- `grep -ci claude_plugin_root` A guard_pre_tool.py: `0`; control A hooks/hooks.json: `19`; wave-5 native_context, inject_context, stage_guard: `0`; control wave-5 hooks.json `19`
- `git merge-tree --write-tree` A+B, A+main, B+main, A+wave-5, B+wave-5: each a single tree id, no conflict
- B `scenario_walk.py --witness-for <owns>`: the 22 files listed in B1

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "A1: test_runtime_paths.py k5 E5 row passes an explicit root, so the env can never matter; call script_command with the default root under the patched env and compare with script_command(name, package_root())",
    "A2: test_refusal_registry.py part_door_texts :141-147 pins brief_pack.py source by AST call count (TESTING.md source pin); replace with a behaviour check: patch RP.package_root to a dollar root and assert command_card_lines head equals script_command('<script>', must_exist=False)",
    "A3: no changelog.d fragment on either branch (builder-rules 11); owns omitted it - add one fragment per part or one at integration",
    "A4: guard_pre_tool.py :825 and :878 inline the lazy import while eight sites use _door_command - route them through it; brief_pack.py :66-71 comment still calls SCRIPTS what the role's Bash uses although it has no product reader now - reword",
    "B1: Part B mechanical layer attaches 4 of the 22 files scenario_walk --witness-for prints; attach the run of the remaining non-quarantined non-slow files or the branch pipeline result"
  ],
  "class_completeness": "Class: a path a role needs is given, never an unexpanded host variable. Axis 18 covered (10 process rows lowered to the measure, no raise). Axis 19 covered (role_has_bash). Axis 32: _host_root_lines scans string constants, not refusal sites, no census unit. Axis 34: E3c makes card and door one spelling. Axes 3/8 do not host the package root; axis 37 stays queued to the full Lead (F7). OH5-2d/OH5-2e known; plan-review B2 carrier still owed at Part A acceptance. Reported analog proposed for OH5-2d's row: brief_pack reads the package root by HERE.parent at 7 spots and the guard by hooklib.PLUGIN_ROOT at 8, beside runtime_paths.package_root (AR-13), owner the coordinator's OH5-2d doc batch.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-254-oh5-2-plugin-root-given.md",
      "docs/tasks/specs/reviews/t-257-oh5-2-plan-review.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md (axis list, axes 32-34)",
      "git diff 18a43b9 origin/wip/oh5-2a",
      "git diff 18a43b9 origin/wip/oh5-2b",
      "git diff 18a43b9 origin/conv/wave-5 -- refusal_registry.py judgment-census.json",
      "oh5-2a: scripts/guard_pre_tool.py :755-830 :1222-1300 PLUGIN_ROOT uses",
      "oh5-2a: scripts/brief_pack.py SCRIPTS sites, :1112-1125",
      "oh5-2a: scripts/tests/test_brief_pack.py :2164-2177 :2255-2275",
      "oh5-2b: scripts/host_adapter.py :519-523",
      "plans/builder-rules.md changelog lines",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B oh5-2a/scripts/tests/test_runtime_paths.py", "result": "101/101 ok"},
      {"command": "python -B oh5-2a/scripts/tests/test_refusal_registry.py", "result": "253/253 ok"},
      {"command": "python -B oh5-2a/scripts/refusal_registry.py --check", "result": "no violations, rc=0"},
      {"command": "python -B oh5-2b/scripts/tests/test_ahead_cards.py", "result": "245/245 ok"},
      {"command": "python -B oh5-2b/scripts/tests/test_role_load.py", "result": "171/171 ok"},
      {"command": "python -B oh5-2b/scripts/role_load.py --all --json vs role-load.json process_ratchet_tokens", "result": "all 12 equal; 10 lowered rows match the dispatch list"},
      {"command": "grep -ci claude_plugin_root oh5-2a guard_pre_tool.py / hooks.json; wave-5 scanned files", "result": "0 / 19; wave-5 native_context, inject_context, stage_guard 0, hooks.json 19"},
      {"command": "git merge-tree --write-tree on A+B, A+main, B+main, A+wave-5, B+wave-5", "result": "all clean, single tree id each"},
      {"command": "python -B oh5-2b/scripts/tests/scenario_walk.py --witness-for <Part B owns>", "result": "22 test files printed; layer attached 4"}
    ]
  }
}
```
