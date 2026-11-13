# t-430 critic: diff gate on OH8-7h (commit 26f7c41, branch wip/oh8-7b)

Scope: ONE commit, 26f7c41 (parent 5e603e4). It adds 21 census rows, lowers the ceiling 21 -> 0, removes the temporary
mechanism (SUBCLASS_UNIT_FILES, SUBCLASS_PENDING_CEILING, C7), and edits the texts of `docs/SIBLING_MAP.md` and
`docs/tasks/critic-diff-brief.md`. Spec: t-346 sections 3.1, 3.5, 4.2, 6a/6b/6c and 10. Mechanical layer: handover t-424.
I did not re-review the rows covered by t-411 and t-423.

## Verdict line per node

- **OH8-7h (t-424): fit_with_fixes. 0 blockers, 3 fixes (F1-F3), plus 1 Lead decision (D1) that may add a fix (F4).**
- DUPLICATION AND CONSISTENCY: one P31 inconsistency. One refusal is classed `safety` in one carrier and `shape` in two
  others (D1). No new code duplication.
- CODE QUALITY: two small items in the changed test, both in F3: an assertion that can never fail, and a column that is
  never read.
- ONE ACTION, ONE ROAD (item 12): the removal closes the temporary second road. Every scanned file now has one road
  (widened site -> unit -> C1). The factory-raise forms are still unseen. They are named in the text (F2 completes the
  list) and have their own node after the chain.

## Control re-run (cheap, on a byte export of 26f7c41)

`git archive 26f7c41 ai-packages/qa-factory | tar -x -C <scratchpad>/t430`, then from `<scratchpad>/t430/ai-packages/qa-factory`
`python -B -m pytest scripts/tests/test_judgment_census.py -q -p no:cacheprovider -s`:

```
census: 279 files scanned, 1141 units; shape=832 xref=195 word-list=0 meaning-proxy=8 meaning=24 safety=82; breach=1; blocks_overrides=10; blocking_per_role: conductor=680 qa-automator=173 qa-bug-reporter=139 qa-case-critic=164 qa-case-designer=139 qa-code-critic=139 qa-doc-scribe=139 qa-failure-analyst=140 qa-requirements-tester=157 qa-retro-analyst=139 qa-runner=140 qa-scout=139 qa-test-strategist=171; subclass_family=55; SCAN_ROOT='scripts' SCAN_EXCLUDE=('tests',)
census breaches: validate_artifacts.py::check_behaviour_claims
24 passed in 94.28s (0:01:34)
```

This matches the handover's final witness: same totals, 24 passed.

## K1. The 21 rows against the six Lead rules

Tally checked independently (k4.py, below): 17 shape, 3 xref, 1 safety; every owner is `data`; no extra keys; no E3 note.

| row | class | my reading |
|---|---|---|
| hooklib.read_config_file | shape | agree. Readable, non-empty, depth, JSON object (rule 4, config) |
| hooklib.story_of | shape | agree on the class for now. Its refusals are flag presence and samefile; the guard is in story_root/story_root_at. Roles: see K3 |
| hooklib.story_root | shape | **reasoning disagreed; the class stands until the 6b node (queue Q1).** Raising condition `if not text.strip() or not is_one_component(text): raise StoryRootError(...)` (hooklib.py:371-373) is a containment guard on a path. The builder says "reads only, writes nothing". That is the function's own behaviour, and it is not the test rule 2 uses: the Lead applied rule 2 to `red_sandbox.inside`, a pure predicate (red_sandbox.py:90-94) whose CALLERS write. The folder story_root returns is written into by artifact_producer, manual_evidence, question_register and others (story_root/story_of callers: 40 files). So by rule 2 this is a written-path guard. In this chain such rows keep their class until the 6b class node (as `_plan_row`, `_hit_repos`, `_clean_stories` did). It must be added to that node's list |
| hooklib.story_root_at | shape | same as story_root. The escape check `raise _no_story(program, shown, "the path reaches another folder, or none, through ..", ...)` (hooklib.py:436-438) goes through a factory, so the scanner does not see it. The function is a unit only through its empty-value raise (:423-425). The class is judged per function, so rule 2 applies just the same. Queue Q1 |
| controller.refresh_derived | shape | agree (the after-commit step did not complete; twin of event_store._run_after_commit, consistent) |
| event_store._require_root | shape | agree. `if self.root.is_dir(): return` ... `raise StoryRootError` (event_store.py:508-521) tests presence, not containment |
| event_store._run_after_commit | shape | agree (twin of refresh_derived) |
| retro_numbers.write_retro | shape | agree (presence of the story folder, :2847) |
| host_adapter.launch_id_keys | shape | agree (a data row readable and of its form, rule 4) |
| role_load._check_kind | shape | agree (closed tokens KINDS, rule 3) |
| role_load._pick_dispatch | xref | agree (the dispatch id resolves in controller.json and its role matches, :555-559) |
| role_load._require_role | xref | agree (closed-token equality against inject-map.json: xref/shape, both legal under rule 3) |
| role_load._task_root | shape | agree. role_load only measures loads and writes nothing downstream, so this is a read path under rule 2 |
| role_load.main | shape | agree (flag combinations) |
| role_load.settings | shape | agree (rule 4) |
| release_fingerprint._unshipped | shape | agree (the git listing exited 0: evidence is present; it reads git state, it does not guard it) |
| release_fingerprint.write_release | xref | agree (recipe files against the git index; the higher of version-form/litter shape) |
| selftest.slow_tests, selftest.test_layers | shape | agree (rule 4) |
| config_view.parse_path | shape | agree (syntax of a config path) |
| story_step.start | safety | **disagree; see K2 (D1).** |

## K2. story_step.py::start (safety) against controller.py::apply (shape)

The raising condition IN `start` (story_step.py:950-963):

```
except IdempotencyKeyReused as exc:
    committed = ...
    if exc.key != "dispatch:" + dispatch_id:
        raise
    ...
    raise IdempotencyKeyReused(f"{exc}. The committed dispatch is not replaced; {write}a NEW dispatch takes a new id ...", exc.key, exc.fields) from exc
```

`start` decides nothing itself. It re-raises with a door, gated on a closed-token equality of the key (rule 3 gives
xref/shape). The refusal is DECIDED in `event_store._commit_locked` (event_store.py:692-694:
`if event["type"] != kind or event["payload"] != payload: raise self._reuse_refusal(...)`). It is re-raised with a text
in `controller.apply` (controller.py:5138-5161). Both existing rows are `shape`. So the same refusal now has three
carriers in two classes. That is a P31 inconsistency, whichever class is right.

Which class: the decider compares one record against another under one key ("one record against another ... a hash
equals", spec 4.2 step 3). That is `xref`. I do not read it as rule 1:
- "a second writer" is a concurrent writer, which the lock already refuses (`event_store.lock`).
- "an overwrite" cannot happen in an append-only journal. The refusal keeps one key meaning one request. It is a join,
  not a guard on bytes.

My proposal (the decision is the Lead's, D1):
- `story_step.py::start` safety -> xref, and `ratchet.safety` 82 -> 81 (a lowering: legal, dense).
- `controller.py::apply` and `event_store.py::_commit_locked` shape -> xref later, in the class node or the 6c fix round.
  This moves no ratchet key: `CLASS_CEILING_KEYS = ("word-list", "meaning-proxy", "meaning", "safety")`,
  test_judgment_census.py:92.

If the Lead keeps rule 1 here, `apply` and `_commit_locked` must move to `safety` too: +2, each raise named. The split
state must not stand past the fix round.

## K3. hooklib roles (builder question 2)

Precedent rows: `hooklib.artifact_root`, `artifacts_dir` and `append_jsonl_line` carry all 12 roles + conductor. `run`
and `run_forms_problems` carry the conductor only. I traced who reaches each new row:
- `read_config_file`: reached from `artifact_root` (hooklib.py:732 `cfg = read_config_file(project) or {}`), whose row has
  every role. **Confirmed.**
- `story_root`: reached from `exit_gate.py:525` `env[DETECTOR_STORY_ENV] = str(hooklib.story_root(task, "exit_gate", ...))`.
  exit_gate is the SubagentStop hook (hooks.json:97-103), so every role's stop passes through it. **Confirmed.**
- `story_root_at`: reached from `planning_contract.py:388-390`, which reads the env var exit_gate sets, so it runs in the
  detectors of the hook. **Confirmed.**
- `story_of`: reached ONLY through `story_cli` (hooklib.py:499). Its callers are role-run and conductor CLIs
  (judge_*, manual_capture, manual_evidence, place_answers, ...). None of the 15 hook entry scripts calls it (the
  `*.py` list of hooks.json against the `story_cli(|story_of(` caller list). So rule (ii) "every role on a hook path" is
  **not** met; this is a (ii)/(iii) doubt, which spec 4.2 step 4 routes to a question.
  - Conductor-only would under-count: role CLIs really do call it, which is the unsafe side.
  - So the row stays all-roles for now, and story_of goes to the 6b roles class node (queue Q2).
  - Effect if that node narrows it: each role key changes by the count of roles it drops, named there.

## K4. AR-20 reconciliation

My own count (k4.py, a pure read of `git show 26f7c41^:<fixture>` and `26f7c41:<fixture>`):

```
rows old/new: 1120 1141 new: 21 gone: [] changed: []
classes of new: {'shape': 17, 'xref': 3, 'safety': 1}
key safety 81 -> 82 new rows of that class: 1
bpr conductor: 659 -> 680 delta 21 new rows naming it 21 OK
bpr qa-* (12 role keys): each delta 4, new rows naming it 4 OK
```

This agrees with the handover's reconcile output and the commit message's raise list key by key:
- conductor +21, every role key +4 (the four hooklib rows), safety +1. No other key moved.
- No existing row changed. No key was lowered by the removal: the two removed constants were never `ratchet` keys.

The fixture's 21 pre-existing local misorders are unchanged in old and new; the new rows are inserted in order. **K4 holds.**

## K5. The removal

- **Still red for a new rowless widened refusal? Yes, unconditionally, for every scanned file.**
  - `units_of` computes `wide = refusal_registry.sites(..., files=sorted(trees), raises=family)` over every scanned file
    (test_judgment_census.py:222-226).
  - It creates a unit from EVERY widened site: `for s in wide_by_file.get(file, []): add(file, s["function"], "u3")`
    (:244-245). There is no list and no condition.
  - `_c1` then names it: `"... is a check unit (u3) with no row ..."` (:309).
  - On the real package, `test_c1_every_unit_has_a_row_and_every_row_a_unit` (:499) fails.
  - Synthetically, the `neutral_only` branch of `test_neg_subclass_raises_flip_blocks_and_create_units` (:776-783)
    proves it.
- **Widened is a superset of literal**, so dropping the literal-only `seen` loses nothing. `_raised_here` keeps
  `func.id in REFUSAL_RAISES` for any spec (refusal_registry.py:1072), and `deny`/`block` calls do not depend on
  `raises` (:1083-1085). The unit count is 1141 before and after, which is consistent.
- **Leftovers:** none.
  - grep -i of `pending|unit_files|\bC7\b|list_problems|sites_by_file|listed|OH8-7b|SUBCLASS_` over the new test finds
    only the negative needles of `test_blind_spot_states_the_subclass_clause` (:829, :834). Positive control: the same
    grep finds `SUBCLASS_ROWS` (:753).
  - The `analyse` docstring says C1..C5 (:437). No parameter, helper or docstring refers to C7.
  - `units_of` no longer returns `pending`/`list_problems`. Its only external reader, `tools/source_split.py:2196-2199`,
    reads `totals["counts"]` and `totals["blocking_per_role"]` only. I checked.
- **The two removed tests:**
  - `test_c7_the_subclass_pending_set_is_dense_and_only_shrinks` was the real-package C7. Its property, an unclassified
    refuser is red, is now carried by C1 (`test_c1_...`). The "dense count" part is gone with the mechanism, legitimately.
  - `test_neg_pending_is_dense_and_only_shrinks_c7` was the synthetic ceiling and the list-form E4/E5 checks. All of it
    belongs to the removed constants. Its one surviving property, a new subclass-only refuser is red, is now the
    `neutral_only` assertion.
  - The removed `listed_unrelated/listed_shadowed_local/listed_tests_only/listed_no_arg` rows (a NEUTRAL function with a
    non-family raise is not a unit) are now covered only by implication: one `wide` list drives both creation and the
    flip, so `blocking == 0` on the `check_f` miss rows implies the raise is no widened site. The direct check is weaker
    than before. F3 restores it cheaply.

## K6. Text carriers

- `git grep -n -i -E "subclass_unit_files|subclass_pending|pending_names" 26f7c41 -- . ':!docs/tasks' ':!plans/piles' ':!logs'`
  finds only test_judgment_census.py:829 (a negative needle). Positive control with the same flags, `meaning_ceiling`,
  finds SIBLING_MAP:390, :561 and critic-diff-brief:72.
- `\bC7\b` over CLAUDE.md, PROJECT.md, .claude/agents, PROCESS, tools, SIBLING_MAP, the brief, design/ and changelog.d
  finds only tools/language_sites.py (its own C7) and tools/source-split-carriers.json:41 (an unrelated id). Control:
  `\bC5\b` finds test_judgment_census.py:250.
- The SIBLING_MAP axis 18 text is rewritten with no constant names, and axis 34's line is gone. The axis 32 row never
  named C7. Brief questions 9 and 11 dropped the names. architecture.md and calibration check 41 name no constant (grep
  `subclass|pending|widened`: unrelated hits only).
- **Leftover (F1):** `ai-packages/qa-factory/changelog.d/oh8-7-census-subclass-raises.md` still says *"a function that
  refuses only that way is counted as pending under a shrink-only test constant and is classified by the follow-up
  nodes"*.
  - This is release text. The next release ships OH8-7 and OH8-7h together, so it will describe a mechanism the package
    no longer has.
  - The DoD grep pattern does not match this prose: "pending" and "subclass" sit on different lines, and the pattern only
    looks for constant names.

## K7. The blind-spot text

- The claim is worded as not complete, and it sits where a reader meets it:
  - the docstring BLIND SPOTS paragraph (:34-45);
  - `BLIND_SPOT`, which is printed with the totals (I saw it in the re-run);
  - the fixture `about`.
- All three say "every WIDENED raise site creates a unit". None says every refusal site. All three name the
  factory-function form with "52 rowless functions ... on 097f58d (an upper bound)".
- Gaps (F2):
  - (a) **The method/attribute factory form is missing from the "still unseen" list.**
    - `raise self._reuse_refusal(...)` at event_store.py:694 returns `IdempotencyKeyReused`, a StateConflict
      subclass (:650, :684). `_raised_here` cannot see it: an Attribute whose value is `self` is not in `mods`
      (refusal_registry.py:1077).
    - The text scopes the form to "a module factory function", and the 52 counts only that form.
    - My overapproximating probe on the export counts rowless functions with `raise <obj>.<lowercase>(...)`: 43, none of
      them in the name-form set. This counts every lowercase callee; return types are not checked, and many are driver
      control flow, not the family. It shows the form exists beyond the one example; it does not count it.
    - The list therefore reads as exhaustive but is not.
  - (b) The docstring says "the scanner does not see that form, and it measured 52". The subject "it" reads as the
    scanner, but the Lead measured it with the critic's script.
  - (c) The number 52 has no counting carrier beside it (hygiene 6(b)). A pointer to spec t-346 §6b, which names the
    script and the commit, is enough.

## K8. Duplication, code quality, class completeness

- Duplication: the change adds no new code duplication. The three-carrier blind-spot text (docstring, BLIND_SPOT,
  `about`) was already there, and `test_blind_spot_states_the_subclass_clause` asserts all three. The one consistency
  defect is D1.
- Code quality (F3):
  - (i) `assert not _has(r["problems"]["C1"], "helpers_x.py::f is a check unit")` (:788) can never fire: no non-neutral
    row defines `f`. Spec 3.5 item 3 prescribed it, so this is a spec artifact. My probe on the export shows that
    `r["problems"]["C1"] == []` holds for all 17 non-neutral rows, so `assert not r["problems"]["C1"]` is a real
    replacement.
  - (ii) The `blocking` column of `neutral_only` (0) is never read, because of the `continue`.
- Class completeness against SIBLING_MAP:
  - Axis 18: covered (member text).
  - Axis 34: covered (row line removed).
  - Axis 32: covered (one scanner; rows in the same commit).
  - Axis 1: covered (critic brief q9/q11; CLAUDE.md rule 10 and designer rule 1 name no constant; I grepped).
  - The release carrier `changelog.d` sits on no axis, but it is the package's own text (FR-37 class): F1.
  - Siblings of D1 (the two other carriers of the same refusal) and of the rule 2 reading (story_root family) are outside
    this commit and queued below.

## Fix list (a fresh builder can execute it; one fixture writer at a time, so it goes into the 6c fix round)

- **F1** `ai-packages/qa-factory/changelog.d/oh8-7-census-subclass-raises.md`: replace the clause *"and the census flips
  `blocks` on the units it already holds; a function that refuses only that way is counted as pending under a
  shrink-only test constant and is classified by the follow-up nodes"* with *"and every such raise site is a check unit
  that needs its census row, like a literal raise (OH8-7..OH8-7h classified the 190 functions that refused only that
  way)"*. Witness: a DOC-DISPATCH key run that shows "pending" absent and "census row" present in the file, with a
  negative control.
- **F2** `ai-packages/qa-factory/scripts/tests/test_judgment_census.py`, in the docstring BLIND SPOTS paragraph and in
  `BLIND_SPOT`, and in `scripts/tests/fixtures/judgment-census.json` `about`: after the module-factory clause, add "or of
  a call to a method or attribute that returns one (`raise self._reuse_refusal(...)`, event_store.py)". Keep the 52 as
  the module-function count. In the docstring, change "and it measured 52" to "and the Lead measured 52 (spec t-346
  §6b)". Keep the token `factory function` (asserted at :826). Witness:
  `python -B -m pytest scripts/tests/test_judgment_census.py -q -p no:cacheprovider` green (24).
- **F3** same test file, `test_neg_subclass_raises_flip_blocks_and_create_units`:
  - (a) replace :788 with `assert not r["problems"]["C1"], (case, r["problems"]["C1"])`;
  - (b) set the `neutral_only` row's third column to 1 and assert
    `rowed["totals"]["blocking_units"] == blocking` instead of the literal 1;
  - (c) optional, the direct coverage the listed_* rows had: for each miss row, also run its body with `check_f` renamed
    to `f` and an empty census, and assert C1 is silent.
  - Same witness as F2.
- **F4** (only after D1): `story_step.py::start` class per the Lead's answer, with `ratchet.safety` moved by the same
  count and named in the commit message.

## Lead decisions (the tier above; not decided here)

- **D1** One refusal, one class: `story_step.start` / `controller.apply` / `event_store._commit_locked`. Recommendation:
  xref for all three, start now (safety 82 -> 81), the two existing rows in the class node with no ratchet effect. The
  alternative is safety for all three (+2).
- Builder question 3: confirm the rule 2 reading. A guard on a path that CALLERS write is a written-path guard, as with
  `red_sandbox.inside`. Then Q1 follows.

## Queue items (findings, D-0044)

- **Q1** The 6b written-path class node gains `hooklib.story_root`, `hooklib.story_root_at` (escape check via `_no_story`)
  and `hooklib.story_of`.
- **Q2** The 6b roles class node gains `hooklib.story_of`: it is reached only through `story_cli` by role and conductor
  CLIs, never by a hook entry.
- **Q3** The factory-function scanner node after the chain must also cover method/attribute factories (`raise self.x(...)`).
  The spec says it creates pending units, so its count must include this form.
- **Q4** Builder analogs worth a finding:
  - `role_load._task_root` swallows `(OSError, ValueError, AttributeError)` from `artifact_root` and falls back to the
    default folder (role_load.py:536-541). That is an FR-59/AR-28 unknown read as a default, and it contradicts
    hooklib.artifact_root's own promise at :730-731.
  - `refresh_derived` and `_run_after_commit` give two texts for one fact.
  - `selftest.slow_tests` and `test_layers` repeat the same read pattern.
- Still open from 6c (not this commit): `question_register.record_case` -> xref, `person_words._from_file` -> safety/intent,
  in the same fix round as F1-F3.

## Trail

Read:
- `git show 26f7c41` (message and full diff of the 4 files);
- spec t-346 §3.5 and §4.1-4.3, §6a-6c;
- handover t-424;
- the critic brief diff;
- review t-423 (the verdict block form);
- on a byte export of 26f7c41: test_judgment_census.py:209-283 and grep hits; refusal_registry.py:1065-1089 and :1185-1214;
- the raise sites of all 21 functions (via raises.py), plus:
  - story_step.py:935-975
  - controller.py:5135-5170
  - event_store.py:23-35, :505-570, :650-700
  - hooklib.py:349-368, :488-500, :726-735
  - exit_gate.py:520-527
  - planning_contract.py:384-391
  - red_sandbox.py:90-94
  - hooks.json (entry scripts)
  - tools/source_split.py:2187-2199
  - tools/source-split-carriers.json
- SIBLING_MAP axis 32 at the commit.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 changelog.d/oh8-7-census-subclass-raises.md still says a subclass-only refuser is counted as pending under a shrink-only test constant: rewrite the clause to say every such raise site is a check unit needing its census row (release text, FR-37 class)",
    "F2 test_judgment_census.py docstring BLIND SPOTS, BLIND_SPOT and fixture about: add the method/attribute factory form (raise self._reuse_refusal(...), event_store.py:694) to the still-unseen list; fix the subject of 'it measured 52' and point the count to spec t-346 section 6b; keep the token factory function",
    "F3 test_neg_subclass_raises_flip_blocks_and_create_units: replace the assertion at :788 that can never fire with assert not r['problems']['C1'] (probe: C1 empty for all 17 rows); give neutral_only blocking=1 and assert rowed blocking_units == blocking; optional neutral-name variants of the miss rows",
    "F4 after Lead decision D1: story_step.py::start class aligned with controller.apply and event_store._commit_locked (recommended xref, ratchet.safety 82 -> 81, named)"
  ],
  "class_completeness": "Axes 1, 18, 32 and 34 covered by the commit. Release carrier changelog.d fragment left stale (F1). The same refusal carried by story_step.start (safety), controller.apply and event_store._commit_locked (shape): one class needed, Lead decision D1. The rule 2 reading (a guard on a path callers write) puts hooklib.story_root, story_root_at and story_of on the 6b written-path class node (Q1); story_of roles go to the roles class node (Q2); the method-factory raise form goes to the factory-scanner node (Q3). The removal leaves no dead constant, parameter, helper or C7 text (grep with control).",
  "trail": {
    "read": [
      "git show 26f7c41 (message + diff of judgment-census.json, test_judgment_census.py, docs/SIBLING_MAP.md, docs/tasks/critic-diff-brief.md)",
      "C:/QAFactory/forge-repo/docs/tasks/specs/t-346-oh8-7b-chain-spec.md sections 3.5, 4.1-4.3, 6a-6c",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reports/t-424-oh8-7h-handover.md",
      "C:/QAFactory/forge-repo/docs/tasks/specs/reviews/t-423-oh8-7fg-diff-review.md (verdict form)",
      "26f7c41 export: scripts/tests/test_judgment_census.py, scripts/refusal_registry.py:1065-1214",
      "26f7c41 export: story_step.py:935-975, controller.py:5135-5170, event_store.py:23-35/505-570/650-700, hooklib.py:349-500/696-735, exit_gate.py:520-527, planning_contract.py:384-391, red_sandbox.py:90-94, role_load.py, release_fingerprint.py, retro_numbers.py, host_adapter.py, config_view.py raise sites",
      "26f7c41: hooks/hooks.json, tools/source_split.py:2187-2199, tools/source-split-carriers.json, changelog.d/oh8-7-census-subclass-raises.md, docs/SIBLING_MAP.md axis 32, design/architecture.md, PROCESS/WEEKLY_CALIBRATION_PROTOCOL.md check 41"
    ],
    "reruns": [
      {"command": "git archive 26f7c41 ai-packages/qa-factory | tar -x -C <scratchpad>/t430; (cd <export>/ai-packages/qa-factory && python -B -m pytest scripts/tests/test_judgment_census.py -q -p no:cacheprovider -s)", "result": "24 passed in 94.28s; census 1141 units, safety=82, conductor=680, each role +4 as declared, subclass_family=55"},
      {"command": "python -B <scratchpad>/k4.py old.json new.json (fixture at 26f7c41^ and 26f7c41)", "result": "new 21, gone 0, changed 0; 17 shape / 3 xref / 1 safety; safety 81->82 (1 row); conductor +21 (21 rows); 12 role keys +4 each (4 rows) all OK"},
      {"command": "python -c probe: _run each non-neutral SUBCLASS_ROWS case with the check_f row (export)", "result": "C1 == [] for all 17 rows"},
      {"command": "python -B <scratchpad>/factory.py <export> (rowless functions with raise <lowercase callee>(...))", "result": "73 name form (overapprox; exploration.py::acquire in it), 43 attribute form not in the name set"},
      {"command": "git grep -n -i -E 'subclass_unit_files|subclass_pending|pending_names' 26f7c41 minus docs/tasks, plans/piles, logs; control meaning_ceiling", "result": "only the negative needle test_judgment_census.py:829; control hits SIBLING_MAP:390/561, brief:72"}
    ]
  }
}
```
