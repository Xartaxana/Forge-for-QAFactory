# t-339: critic diff gate for OH8-2a, OH8-2b and OH8-6 (one topic, R13-g)

Critic (Opus), 2026-11-13. The DoD is spec `docs/tasks/specs/t-324-oh8-2-oh8-6-spec.md` (§0a, §0b, §1-§7) and its plan review t-328. Diffs: 2a `fd6e0f4..7f10279`, 2b `b769c9d..4151df2`, OH8-6 `b7d1e8a..9f2e6df`. I read the worktrees `.claude/worktrees/oh8-2a|oh8-2b|oh8-6`.

## Verdict per node

| Node | Verdict | Blocking | Fix-now | Follow-up |
|---|---|---|---|---|
| OH8-2a | **fit_with_fixes** | 0 | F1 | F9, F10 |
| OH8-2b | **fit** | 0 | — | — |
| OH8-6 | **fit_with_fixes** | 0 | F2, F3, F4, F5, F6 | F7, F8 |

Overall: **fit_with_fixes, 0 blocking findings.** I found no regression of an exact key, no fail-open in the guard, and no change to a money total. The fixes are small, and all of them sit in files the nodes already own, except where I say so. Accepting the work is the coordinator's decision (rule 6).

## Findings

**F1 (2a, fix-now minor): the POSIX cells for the one named behaviour change are missing.** `test_resolver.py` `_oh82_world` (2a :1782-1817) has no exact-folder `v1.` cell and no "`T` and `t` both real" cell. Both are required by spec §5 (`OH82_NAMES`, POSIX) and §3 I2/B3. The `v1.` cell pins the ONLY behaviour change of an exact key (I2 exception: `is_story_folder`, `story_root` and `artifacts_dir` all refuse it). I traced the code and it is correct: `clean_key('v1.')` is False, so `is_story_folder` is False, `story_root` gives `_no_story`, and `artifacts_dir` refuses on shape. But no test holds it, and CI (Linux) is where the cell would run. The "both real" cell pins "exact wins" (`t` in the listing gives the path at hooklib :297). **Fix:** add both cells under `os.name != "nt"`. Expected: `v1.` is refused by the three leaves and gives no-story at the gates; `t` is accepted as exact and `T.` is refused on shape.

**F2 (OH8-6, fix-now; integration order): `test_resolver.py` is red on the OH8-6 tree, and the OH8-6 witness does not show it.**
- My rerun: `python -B .claude/worktrees/oh8-6/.../tests/test_resolver.py` gives `FAIL OH8-2 sentinel: the allowance is not stale (shrink it) ... 'cost_capture.py': 1` and `=== test_resolver: 956/957 ok ===`.
- Cause: main a4a233c (OH8-3 fd75410) cut `cost_capture.py` to 1 call, but 2a's `OH82_ALLOWED` says 2 (7f10279 :2033). The merge base b7d1e8a carries that stale allowance, and 2b fixes it (4151df2 :2160).
- `scenario_walk --witness-for` over OH8-6's owns lists `test_resolver.py` (my rerun, lines 53 and 160 of its output). The OH8-6 report says "non-slow witness files green" but names no `test_resolver` result. That is a witness claim I could not reproduce (critic rules 7 and 12).
- **Fix:** merge 2b into main BEFORE OH8-6, or merge 2b into wip/oh8-6 and re-run `test_resolver.py` as part of its witness. The OH8-6 report gets the corrected line. The same red sits on a bare 2a+main merge (b769c9d), so 2a must not land alone without 2b's allowance line either.

**F3 (OH8-6, fix-now; I5 neighbour on the same surface): a non-object activity spool still tracebacks out of `record`, and the receipt is lost.**
- The surface is "a host hook reading a local state file" (I5: "a broken file never stops the new receipt").
- `host_dispatch.record` :347 calls `doc = load(activity_path(...))`. `activity_capture.load` (:66-67) returns any JSON, so `[]` reaches `doc.get` and an entry `5` reaches `a['activity_id']`.
- My probe on the OH8-6 tree, `record(spawn)` with `state/activities/parent.json`:
  - `[]` gives `RAISED AttributeError 'list' object has no attribute 'get'`;
  - `{"activities":[5],"active_stack":["x"]}` gives `RAISED TypeError 'int' object is not subscriptable`.
- `main` (:382-386) has no wrapper, so `atomic_json(binding_path…)` never runs.
- The same `load` feeds `close_pending` (a Stop capture). Spec 4c marked activity_capture:63 "guarded", but that covers decode errors only, not shape.
- C5 fixed the migration read of this very file, so the class is half-covered.
- **Fix (class level, AR-13):** `activity_capture.load` reads through `hooklib.read_json(path, None, kind=dict, errors=Exception)` and falls back to its default doc. Also, `record` :348 skips non-dict entries (`isinstance(a, dict)`). `load` is in an owned file but not in OH8-6's function list, so the coordinator widens the owns by one function. Add a row with `[]` and a non-dict entry to `BrokenReceiptTable`.

**F4 (OH8-6, fix-now; money attribution, one road): the two "nothing inherited" worlds of C6 attribute the same session differently.** Empirics (my probe through `BrokenReceiptTable.cost`, 7 cells):

```
none         subtotal=0.00382 orch=0.0038 attr=-                        by_activity=[act-story 1200, unclassified 230]
{ / []       subtotal=0.00382 orch=0.0038 attr=...unreadable            by_activity=[act-story 1200, unclassified 230]
activity 5   subtotal=0.00382 orch=0.0038 attr=...has no usable activity by_activity=[act-story 510, unclassified 920]
segments []  subtotal=0.00382 orch=0.0038 attr=...has no usable activity by_activity=[act-story 510, unclassified 920]
{} / valid   subtotal=0.00382 ...                                       ({}: 1200/230; valid: 510/920)
```

- The total is unchanged on every branch (see the C6 note below).
- But in the shape-failure cells, `binding['activity']` stays truthy (5, or a dict with no segments). So cost_capture :2052 `... if person_rule and not binding.get("activity") ...` SKIPS `start_turn_activities`, although nothing was inherited. The session lands in a third world: neither inherited nor start-turn. An unreadable receipt gives 1200 tokens to act-story; an unusable one gives 510.
- Both are marked `incomplete`. Still, that is two roads for one state (P31, AR-15), on a money line. Spec C6 said "activities is not replaced" and did not name :2052.
- **Fix:** keep a local `inherited = True` only where `activities = [inherited]` is assigned, and test `not inherited` at :2052 instead of `not binding.get("activity")`. `binding` stays in `key_inputs` as the spec decided. :2052 lies outside "the host_binding block only", a one-line owns widening for the coordinator. Add a cell asserting that the shape-failure `by_activity` equals the unreadable cell's.

**F5 (OH8-6, fix-now minor): C1 can signal one broken path twice.** In `record` :266-274 (SubagentStop), with `host_binding` set, both identities use the SAME `path`, and `_unreadable(event, path, …)` is called with no `said` set. When there is no session id, or no onboarded project (stderr last resort), the person reads it twice. The spec's "one person_signal per broken path" holds only through `person_signal`'s once flag. **Fix:** create `said = set()` before the loop and pass it. Add a C1 cell with `host_binding`.

**F6 (OH8-6, fix-now minor; code quality, brief item 7):**
- `record` (:257-379) is about 123 lines. The new C3 block (:351-378) nests 3 levels, with a 3-clause shape condition (:373-374).
- The text "`story_step.py bind` ties it later" is built 3 times, and the config path twice (:325, :355).
- `_unreadable`'s `try/except Exception: pass` (:252-255) is dead: `hooklib.person_signal` documents and implements "NEVER raises" (hooklib :2686-2716).
- **Fix:** extract `_controller_dispatch(folders, task, role, event, said) -> str | None` from :351-378, and drop the dead try. No behaviour change; the existing table holds it.

**F7 (OH8-6, follow-up, target pile `cost-dashboard`; deviation 6): `telemetry_coverage.attribution` has no reader. Neither does `telemetry_coverage` as a whole.**
- `grep -rn telemetry_coverage` over the package (`--include=*.py,*.md,*.json`, tests excluded) hits only `cost_capture.py` :1983 and :2311, the writer (my positive control) and the changelog.
- So the spec's premise "so the report prints the gap" (C6, FR-41, P18) is false for that field. The gap reaches the report only as a COUNT of `host_receipt_unreadable` in `report_facts._hook_signals` (:2770), and the price is not printed as a range.
- This is not new in kind: `provider_usage` and `external_usage` are equally unread. So the AR-22 breach is pre-existing for the dict and extended by one key. It does not block this node: the session total is right, and the signal lands in the run report.
- **Proposed node (owner: the cost-dashboard Lead; the coordinator opens it, rule 19):** the report and the dashboard read `telemetry_coverage` (all keys), and a story whose sessions carry `attribution: incomplete` prints its price as a range "от … до …" with the mark (P18). The OH8-6 commit line "AR-22 -- the SCOPE prose follows SCANNED" should not be read as covering this field.

**F8 (OH8-6 / 2a, follow-up, onboarding-hooks next batch; duplication, brief item 6):** `vcs_evidence.py:595-596` is a sixth copy of `is_story_folder(...) and (... / "pipeline.json").is_file()`, which `hooklib.is_story_with_pipeline` (2a :392) now owns. Grep: `grep -A1 'is_story_folder('` with `pipeline.json` over `scripts/*.py`, after 2a. Hits: hooklib :396 (the leaf, my positive control) and vcs_evidence :596 only. The answer is the same (exact), so it is not a bug. **Fix:** call the leaf. Line for «Остатки»: `vcs_evidence._story_of: call hooklib.is_story_with_pipeline | узел: <next OH node>`.

**F9 (2a, follow-up for the Lead; axis 8): the map row has not moved.** `docs/SIBLING_MAP.md` :222 ("The ONE key -> story-folder rule") does not name `clean_key`, `other_spelling`, `landing_name`, `alias_twins`, `is_story_with_pipeline`, the new `artifacts_dir` refusal, or the readers A7-A17 / B1-B6. Spec §7 says "The Lead edits the map with 2a". I grepped `clean_key|other_spelling|landing_name` in the map in all three worktrees and in read-main: 0 hits. As my positive control, the same file has 1 hit for `is_story_folder`. This is the Lead's move in the integration commit (rule 9: a new symmetry goes into the map in the same commit), not a builder defect.

**F10 (2a, follow-up for the coordinator; class completeness): the §8 analogs have no pile carrier.** Spec §8 items 1-7, 9 and 10 (session-id/pin-key uses, exploration slugs, manual_capture names, CLI tracebacks, exit_gate `NOPE`, cost_capture:1963, the `_STORY_RE` literal, execution_scheduler:156, `_story_names` -> `landing_name`) do not appear in `plans/piles/onboarding-hooks/` (read-main 2182255). I grepped for `_story_names|execution_scheduler|1963`: the only hit is the old OH5-12 / B-298 row, which is closed and a different class. Each gets a row in «Остатки» per brief item 4 (`| узел:` or `| перенос: … | подтвердил: —`). F3, F4 and F8 above join them if they are not fixed in this round.

## Builder-declared deviations

1. **2a A6, `story_root` :447 shape gate without `clean_key`: accept.** I traced it: after the shape gate, the only return is `if is_story_folder(path.parent, text): return path` (:470), and `is_story_folder` calls `clean_key` (:387). So `T.`/`T `/`v1.` always end in `_no_story`, which names the near miss `T` through `alias_twins` (:419). No route returns another story's folder. B8/B9 keep their text. The "same answer" of B3 holds as "both refuse", with two texts (shape vs no-story): acceptable.
2. **2a `landing_name` skips an entry whose samefile raises: accept, and it is the better direction.** Under the spec's "any error gives ''", one broken symlink or locked entry in the listing would make `landing_name` "" for EVERY alias. The guard would then judge the raw key, which is the B1 fail-open class. The skip still returns only a samefile-True name (OS truth), and the outer try still gives "" on a listing failure. The spec text should be updated to match (Lead).
3. **2a: a leading blank is shape-refused only; `QA_FACTORY_TASK` is stripped but the explicit id is not: not a P31 finding.** The `.strip()` at stage_guard :601 predates this diff. It normalizes a person's shell word to the exact key, and the shared leaf `is_story_with_pipeline` is reached on both roads (rule 19: an ordinary condition of the task, with the shared mechanism reached). A leading blank on NTFS is not dropped (` T` is a different folder), so `clean_key` refusing it costs nothing and is uniform across OSs (AR-4). The test row `resolve_ticket_env` pins this on purpose.
4. **2a guard alias judgment is OS-dependent: accept.** There is one road, `os.path.samefile` (no `os.name` branch in `_path_story` or `landing_name`). The outcome differs because the file system does: on a case-sensitive disk, a write to `t/` really lands in a new folder `t`, not in `T`. I3 ("a write the OS lands in T is judged by T's rules") is exactly this. `artifacts_dir` still refuses `t` on every OS through the casefold twins.
5. **OH8-6: the controller-shape signal fires on shape defects as well as read failures; an absent `dispatches` or `{}` is silent: accept.** It fits FR-4 (a shape the lookup cannot use is an informed pass, not a silent one). An absent key or empty dict is a legitimate controller state (no dispatch yet). `test_controller_shapes_name_no_dispatch` pins the 9 rows.
6. **OH8-6: `telemetry_coverage.attribution` has no reader:** a named follow-up, not a fix in this node. See F7.
7. **2b B5: the join moved after the check (a non-str task no longer raises TypeError): accept.** A journal `task` of 5 used to crash `a5_seal` on `artifact_root()/5`. Now `is_story_folder` gives False and the task is skipped. Such a record names no folder, so nothing auditable is skipped. An unhashable task still fails earlier (`task not in seal`), which is pre-existing and outside the owns.

## C6 money: empirics first

I ran the probe above before reading code. `priced_subtotal_exact_usd` is 0.00382 and `orchestrator.cost` is 0.0038 in all 7 cells (no binding, `{`, `[]`, `activity 5`, `segments []`, `{}`, a valid activity). **The session total is unchanged on every branch.** The cost file is written on every path: `atomic_json(output_path, document)` (:2396), with no early return between :1979 and :2396. I read code only where the run diverged, which was attribution (F4). The attached test asserts `sum(by_activity.tokens)` and not money. My probe adds the money fields, and they agree.

## Standing questions

- **1 Fit to the spec:**
  - 2a: A0-A17 implemented as written. I checked A1 order (:291-306), A2b composition (:349-357), A13 placement inside the explicit-id branch (:255-268), and the 8 `_STORY_RE` sites. Only `story.group(0)` splitting remains at :1305/:1319. The gaps are F1 and deviations 1-2.
  - 2b: B1-B6 as written.
  - OH8-6: C1-C6, C2' and C3' as written. The gaps are F3, F4, F5 and the spec premise in F7.
- **4 Class completeness (axis 8):** the readers named by the spec are covered. The leaf composition is one survivor: `other_spelling` is used by `artifacts_dir` and `_identity`, and `landing_name` by the guard. I ran the widened problem grep `artifact_root\([^)]*\)\s*/\s*(str\()?[\w\[\]"']*(task|ticket|story|key|name)` (-P -i) on the 2b tree. My positive control `execution_scheduler.py:156` hit. All 34 hits are rows in §2 or in-diff, except `red_sandbox.py:1407`. That one is not a key reader: it compares `resolve()`d paths, so it is n/a and a spec fact gap only. Open: F9 (map row) and F10 (no carrier for the analogs).
- **5 Tests:** the `OH82_ROWS` table with spies would catch the defect on the old code on Linux too: the spy requires the leaf to be asked. The red-on-old figures are 863/903 (2a) and 1021/1145 (2b), consistent with the spies. `BrokenReceiptTable` reruns OK. The gaps are F1, F4 and F5.
- **6 DUPLICATION AND CONSISTENCY:**
  - F8 (vcs_evidence copy) and F6 (repeated texts).
  - `_no_story` converged on `alias_twins` (2a :419).
  - What I grepped: `is_story_folder(` with `pipeline.json` (control: hooklib :396), `_STORY_RE|story.group` and `re.compile.*artifacts` (control: guard :959; the other hit, `check_witness.py:74`, is an evidence path, not a key), and `json\.loads?\(` in host_dispatch/activity_capture (remaining hits :162 and :288 are inside try; activity_capture :67 is F3).
- **7 CODE QUALITY:**
  - F6 (`record` length, nesting, a dead try).
  - The 2a helpers are short, never raise, and their docstrings are true. `_identity` grew by 14 lines at nesting level 3, which is acceptable.
  - 2b: none found. I read all 5 hunks: no dead branch, and `path` computed before the gate is never read on refusal.
- **9 Ratchets:**
  - census `hooklib.py artifacts_dir`: shape -> xref, named in the 2a judgment line, which is right (it now compares with the listing).
  - `OH82_ALLOWED` is a new shrink-only sentinel. 2b lowers role_load 2->1 and cost_capture 2->1. No raise anywhere.
- **10 ARCHITECTURE:** all three commits name their AR-n. AR-15 is held by one survivor. AR-28 holds: an alias is `unknown-task`, and an unreadable receipt is never marked terminal. AR-13 holds for the receipt reads, but F3 leaves `activity_capture.load` as a second raw reader of a state file. AR-22 is claimed by OH8-6 for SCOPE (held: `part_scope_docstring` plus mutations) but is extended-broken for `telemetry_coverage` (F7, not blocking: no reader is starved; the field is new).
- **11 JUDGMENT (AR-29):** no judgment moved. Every new check is shape or xref over data: `clean_key`, the listing compare, samefile, read_json kind=dict, dict-shape guards. The texts are reports, and none of them closes a role obligation or refuses a role's content. The `judgment:` lines are truthful. No census scan constants or craft markers were touched.
- **12 ONE ROAD (P31):** F4 (two attribution roads for "nothing inherited"). Deviations 3-4 were examined and are not this class. No language or project branch was added. I grepped the diffs for `os.name`: the only hits are in test cells (junction creation, and the nt-only negative control and guard expectation). Production code has none.
- **8 Hygiene:** the changelog fragments are English. I spot-read the three fragments for Cyrillic and found none.

## Trail

Read:
- the spec t-324 (whole) and the plan review t-328 (whole);
- `docs/tasks/critic-diff-brief.md` :8-101;
- `docs/SIBLING_MAP.md` :202-227;
- all three diffs whole (production and tests);
- 2a `exit_gate._identity` :215-300, `hooklib` :425-472, `stage_guard.resolve_ticket` :585-660, `guard_pre_tool.owner_check` :1440-1520;
- OH8-6 `cost_capture` :1940-2010, :2280-2300, :2370-2405, `hooklib.person_signal`/`_once_flag`/`_signal_task`, `host_dispatch` :155-168, :340-390, `activity_capture` :62-80, `report_facts._hook_signals` head;
- `vcs_evidence` :590-605, `check_delivery` :680-695, `red_sandbox` :1395-1412, `controller` :2476-2484;
- the commit messages of the three tips.

Reruns (verbatim tails):
- `python -B .claude/worktrees/oh8-6/ai-packages/qa-factory/scripts/tests/test_resolver.py` -> `FAIL OH8-2 sentinel: the allowance is not stale (shrink it) ... 'cost_capture.py': 1 ...` / `=== test_resolver: 956/957 ok ===`
- `python -B .claude/worktrees/oh8-6/.../tests/test_codex_host.py BrokenReceiptTable` -> `Ran 6 tests in 0.664s` / `OK`
- the C6 money probe (heredoc, temp dirs only) -> the 7-row table under F4
- the activity spool probe -> `[] -> RAISED AttributeError ...`, `{"activities":[5],...} -> RAISED TypeError ...`
- `scenario_walk.py --witness-for <OH8-6 owns>` -> lists `test_resolver.py` and `test_codex_host.py`
- `grep -c is_one_component(` per tree: cost_capture 2/1/1 and role_load 2/1/2 (2a/2b/6)
- the widened problem grep (-P -i) on 2b -> 34 hits, control `execution_scheduler.py:156` present
- `grep -rn telemetry_coverage` over the package -> only `cost_capture.py` (the writer)
- the map grep for the new leaves -> 0 in all four trees

Not rerun: 2a's 903/903 and 2b's 1145/1145 for `test_resolver`. I checked them for consistency instead: the sentinel counts in each tree match what I measured. The slow files are the canon's.

```json
{
  "verdict": "fit_with_fixes",
  "blockers": [],
  "fixes": [
    "F1 2a test_resolver.py _oh82_world: add POSIX cells exact folder v1. (refused by is_story_folder, story_root, artifacts_dir) and T plus t both real (t exact accepted, T. shape refused)",
    "F2 OH8-6: test_resolver red on the OH8-6 tree (sentinel cost_capture allowance 2 vs 1, 956/957); merge 2b before OH8-6 or merge 2b into wip/oh8-6 and attach the test_resolver result to the OH8-6 witness",
    "F3 OH8-6: activity_capture.load returns non-object JSON and host_dispatch.record :347-348 raises (probe: [] AttributeError, entry 5 TypeError), receipt lost; load via hooklib.read_json kind=dict with its default doc, record skips non-dict entries, add table rows; owns widened by activity_capture.load",
    "F4 OH8-6 cost_capture :2052: shape-failure binding skips start_turn_activities though nothing was inherited (by_activity 510 vs 1200 for unreadable); test an inherited flag instead of binding.get(activity); add a cell; owns widened by that line",
    "F5 OH8-6 host_dispatch.record :266-274: pass a said set in the SubagentStop loop so a host_binding path is signalled once; add a C1 cell with host_binding",
    "F6 OH8-6 host_dispatch.record: extract the C3 block :351-378 into a helper, build the bind-later text once, drop the dead try in _unreadable :252-255"
  ],
  "class_completeness": "Axis 8: readers A7-A17 and B1-B6 covered, one survivor other_spelling/landing_name/clean_key; widened grep 34 hits all in spec or diff except red_sandbox:1407 (resolve compare, n/a). Open: SIBLING_MAP :222 row not updated with the new leaves (Lead, integration commit); spec section 8 analogs have no pile carrier (coordinator, Ostatki rows); vcs_evidence:595-596 duplicate of is_story_with_pipeline (follow-up); activity_capture.load is the unfixed I5 neighbour (F3); telemetry_coverage has no reader at all (follow-up node, cost-dashboard pile).",
  "trail": {
    "read": [
      "docs/tasks/specs/t-324-oh8-2-oh8-6-spec.md",
      "docs/tasks/specs/reviews/t-328-oh8-2-oh8-6-plan-review.md",
      "docs/tasks/critic-diff-brief.md",
      "docs/SIBLING_MAP.md axis 8",
      "git diff fd6e0f4 7f10279; git diff b769c9d 4151df2; git diff b7d1e8a 9f2e6df",
      "worktree oh8-2a: exit_gate.py _identity, hooklib.py story_root, stage_guard.py resolve_ticket, guard_pre_tool.py owner_check",
      "worktree oh8-6: cost_capture.py _capture, hooklib.py person_signal, host_dispatch.py record/main, activity_capture.py load, report_facts.py _hook_signals",
      "vcs_evidence.py 590-605, check_delivery.py 680-695, red_sandbox.py 1395-1412, controller.py 2476-2484"
    ],
    "reruns": [
      {"command": "python -B .claude/worktrees/oh8-6/ai-packages/qa-factory/scripts/tests/test_resolver.py", "result": "FAIL OH8-2 sentinel allowance not stale, cost_capture 1; 956/957 ok"},
      {"command": "python -B .claude/worktrees/oh8-6/ai-packages/qa-factory/scripts/tests/test_codex_host.py BrokenReceiptTable", "result": "Ran 6 tests OK"},
      {"command": "C6 money probe via BrokenReceiptTable.cost over 7 binding cells", "result": "subtotal 0.00382 and orchestrator 0.0038 in every cell; by_activity 1200/230 for none, unreadable, {}; 510/920 for valid and for shape failures"},
      {"command": "record(spawn) probe with a non-object activity spool on the OH8-6 tree", "result": "[] AttributeError; entry 5 TypeError; receipt not written"},
      {"command": "scenario_walk.py --witness-for OH8-6 owns", "result": "lists test_resolver.py and test_codex_host.py"},
      {"command": "grep -P -i widened problem grep over 2b scripts", "result": "34 hits, control execution_scheduler.py:156 present"},
      {"command": "grep -rn telemetry_coverage over the package", "result": "only cost_capture.py writer lines and the changelog"},
      {"command": "grep clean_key|other_spelling|landing_name in SIBLING_MAP.md, four trees", "result": "0 hits; control is_story_folder 1 hit"}
    ]
  }
}
```
