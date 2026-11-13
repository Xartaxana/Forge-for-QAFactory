# t-301 — diff critic, OH6-1 (`onboarding-hooks/6/OH6-1`), commit 33b31ee on `wip/oh6-1`

Reviewer: critic (Opus). DoD under review: `docs/tasks/specs/t-282-oh6-1-one-component.md` (§2 sites, §3 positions,
§4 edges, §5 tests, §6 DoD, §7 D-0048 lists, coordinator decision). Diff read whole: `git diff 33b31ee~1 33b31ee`
(13 files, +329/-28).

**Verdict: ACCEPT (`fit`), 0 blocking findings.** This is a proposal. The acceptance decision belongs to the
coordinator of the proper tier (rule 6).

## 1. Sites against spec §2.2 / §3 (error direction and position), traced one by one

| # | site | new code (worktree) | direction kept | position (§3) |
|---|---|---|---|---|
| 2.1 | `is_one_component` | separator literal `"/\\:\0"`; the docstring names NUL; no strip and no length | never raises; errs only toward False | — |
| 2.1 | `is_story_folder` | `not is_one_component(name) or not name.strip() or name != name.strip() or parent is None ...` | equivalent: the old disjuncts `not isinstance`, empty, `.`/`..` and `/\:\0` all sit inside the survivor; a non-str short-circuits before `.strip()` | the survivor runs first. It is a bare global, so the spy sees it (the spy column is green) |
| 1 | `host_dispatch.controller_record` | `if not dispatch or not hooklib.is_one_component(ticket): return None` | None. Old `not ticket` = the survivor's empty check | before `artifact_root(...) / ticket` |
| 2 | `exit_gate._named_ticket` | the comprehension calls the survivor before `is_file()`; module-level `import hooklib` added | name dropped | before the join; `""` no longer probes the root |
| 3 | `stage_guard.story_named_by_text` | `hooklib.is_one_component(name) and ...exists()` | dropped | before the join |
| 4 | `resolve_ticket` env route | `if hooklib.is_one_component(env_task) and ...is_file(): return` | skipped, falls to `_env_exploration` | unchanged order; `explore:<slug>` still reaches `_env_exploration` (read at stage_guard.py, the line after the check) |
| 13 | `resolve_ticket` explicit route | the survivor joins the `is_file()` condition INSIDE `if explicit:` | `("", facts)` | `facts["explicit"]`/`explicit_source` are set before it, the explain block still runs, the block always returns, and no fall-through to the guess. The block is NOT wrapped (the defect §3 forbids) |
| 5 | `_recipient_receipts` | `hooklib.is_one_component(story) and ...is_file()` | receipt skipped | after `binding_names` and the dispatch test |
| 6 | `activity_capture.activity_path` | first statement; ValueError text byte-identical | ValueError | before `project_root` and the legacy move |
| 7 | `cost_capture._capture` | `not tpath.is_file() or not hooklib.is_one_component(session_id)` -> `sys.exit(0)` | exit 0 | before `_session_scope_ok` |
| 8 | `cost_capture.main` | the same -> `return` | return | after the `metadata()` replacement of `session_id`, before `--debounced`, the marker and the lock |
| 9 | `recover_codex_usage.recover` | `if not hooklib.is_one_component(session):raise ValueError('Unsupported session identity')` | ValueError, text kept | after `metadata`, before `scan` |
| 10 | `estimate_record.task_binding` | local `import hooklib` beside the local import; the text is kept | ValueError | first, before `artifact_root(...) / task` |
| 11 | `red_sandbox._row_problem` | `_component` deleted; both `all(...)` call the survivor; `isinstance(v, str) and v` kept; `import hooklib` exists at :82 | the problem strings are unchanged | inside the same `all(...)` |
| 12 | `role_digest.file_notes` | `if not tail or not hooklib.is_one_component(name): return ""`; `import hooklib  # noqa: E402` | `""`, never raises | before `joinpath` and `mkdir` |

The superset invariant of §2.1 holds: no old copy refused anything the survivor accepts. I checked each old
disjunct, including `role_digest`'s `name != Path(name).name` on Windows (`a:b` and `C:` are refused by `:`
in the survivor). I found no import cycle: every import of `hooklib.py` at the top of the module is stdlib,
and its project imports are function-local.

## 2. Class-wide completeness (rule 5; axes 8, 18, 34)

- My own search, as a Grep with `-i` over `scripts/*.py` of the worktree: `in ['"](/\\\\|\\\\/)`. It found
  only `hooklib.py:272` in `scripts/*.py`, which is also the positive control: the survivor itself is found.
  The `.`/`..` tuple and set form found `event_store.py:482` (§2.4), `hooklib.py:272`, and
  `manual_capture.py:295` and `session_identity.py:49`. The last two apply a stricter allow-list, and §2.3
  excludes them. The `!= Path(x).name` / basename form found `event_store.py:482`, `selftest.py:982`,
  `dependency_drift.py:92` (§2.4, the named blind spot) and `reporters.py:455` (not a copy). The `"/" in x or`
  form gave 12 hits; I read them. They are path-vs-name and extension checks. The nearest one,
  `install_paths.py:605` (`rebuilt_by`), is a stricter script-name rule on a data table, not a path-join
  guard, so it is not a copy.
- The §2.4 allowance is exactly the named sites. The sentinel's PATH_NAME hits outside `hooklib` are exactly
  `event_store.py` 1 and `selftest.py` 1. `dependency_drift.py` sits in the stated basename blind spot.
- The remainder is queued, not left silently. On `origin/main` I found these findings:
  - `findings/20261113-is-one-component-kopii-vne-oh6-1.md` names `event_store` (l.11), `selftest` (l.12)
    and `dependency_drift` (l.13);
  - `...ntfs-imena-psevdonimy-...md` (F-3);
  - `...oh6-1-tihij-propusk-vmesto-traceback-...md` (F-8).
- `worker_lifecycle.py:94` already reads through `artifacts_dir` (spec §2.2). The diff does not touch it.

## 3. Standing questions

- **DUPLICATION AND CONSISTENCY (item 6):** no blocking duplication. The diff removes 12 hand copies and one
  helper (`red_sandbox._component`) in favour of the existing survivor. In the test, `_oh61_patched` is a
  hand-rolled `unittest.mock.patch.multiple`. `harness.py` has no generic attribute patcher (`reader_patched`
  at harness.py:361 is reader-specific), and 110 test files use `unittest.mock`. This is a queue-level note,
  not a fix (N2). What I grepped: `contextmanager|def \w*patch\w*\(` over `tests/test_resolver.py` and
  `harness.py`, and `unittest.mock` over `tests/`.
- **CODE QUALITY (item 7):** none blocking. The new functions are short: `oh6_1_sentinel` is about 35 lines,
  the table runner about 20, and each row is 3-8 lines. No dead branches and no lying names. Every row's
  result is read by the judge lambda.
- **ARCHITECTURE (item 10):** the commit names AR-15, AR-13, AR-29, AR-20, AR-28 and AR-4.
  - AR-15/AR-13: one reader, wired at all 13 sites, with a spy proof per cell.
  - AR-20: `OH61_ALLOWED` is shrink-only, with a stale check and an exact-literal check.
  - AR-28: NUL and non-str are refused in each site's own direction.
  - AR-4: `:` and `\` are refused on every OS.
  - No producer or reader was removed while its counterpart stays: `_component` had no other caller (C-6).
- **JUDGMENT (item 11):** shape checks only. The census reran green: 22/22, 949 units, `breach=1`. The single
  breach, `validate_artifacts.py::check_behaviour_claims`, is in a file this diff does not touch. The diff
  does not touch `judgment-census.json` either (`git diff --stat` on both paths is empty), so the breach is
  pre-existing. No census row is added and none is raised.
- **IN-TREE RATCHETS (item 9):** one new ratchet, `OH61_ALLOWED = {"event_store.py": 1, "selftest.py": 1}`.
  It is born at its floor and points to the queued node. Nothing listed in item 9 is raised.
- **ONE ROAD (item 12):** the diff closes a P31 class: one road for "a name is one path component". No
  language, project or case is excluded from it. The remaining roads (§2.4) form a node with an owner, the
  Lead of onboarding-hooks, and that node exists on origin/main. Nothing else found. What I grepped: the four
  copy forms in §2 above.
- **D-0048 lists (hot files):** these match the diff hunks exactly:
  - `hooklib`: `is_one_component`, `is_story_folder`;
  - `stage_guard`: `story_named_by_text`, `resolve_ticket` (both routes), `_recipient_receipts`;
  - `cost_capture`: `_capture`, `main`, plus one `import hooklib` line beside the existing `from hooklib`
    import (C-2: the shared line is not edited).
- **Hygiene (item 8):** `selftest --lang` is 4/4 per the attached layer, and the changelog fragment is English.

## 4. Mechanical layer: consistency and control rerun

- Control rerun, `python -B scripts/tests/test_resolver.py` (package dir of the worktree): `=== test_resolver:
  437/437 ok ===`. `PASS OH6-1` lines: 215. That is 105 table cells + 98 spy cells + 12 sentinel checks, and it
  matches DoD 3 and the builder's numbers.
- The sentinel's controls (5 positive, 1 negative, 2 differential) are all PASS in my run.
- The mutation witness (424/437 with `recover_codex_usage-dotdot` red) is consistent with the table. The
  `..` cell has a planted file (rule 1), so only the guard can refuse it. I did not re-run the mutation.

## 5. Non-blocking notes (none needs a fix round)

- **N1, dispatcher side.** `changelog.d/oh6-1-one-component.md` is outside the spec's 12 owns. The standing
  rule `plans/builder-rules.md` item 11 requires the fragment, so the builder was right. The spec template
  should list the fragment in owns.
- **N2.** `_oh61_patched` re-implements `unittest.mock.patch.multiple`. Optional cleanup; queue-level.
- **N3, test strength.** The spy column asserts `name in seen`, meaning ANY call of the survivor with that
  name during the run, not the site's own call. For creatable names, the outcome column plus the rule-1 plants
  carry the proof. The NUL cells (and `a:b` on Windows) rest on the spy alone, and so on the absence of a
  second survivor call with the same name in the path. I traced the explicit-route explain block
  (`load_config`, `_collect_story_facts(root, task_name, ...)`): it does not pass `explicit` to the survivor,
  so the cell is sound today. This is a known limit, not a defect.
- **N4.** The commit is `tier: sonnet` and adds a machine check (the sentinel) with the four questions
  answered. The mechanism gate scopes mechanism paths, and package tests are not among them as far as I know.
  Whether this commit needs a Lead-tier `tier:` line at integration is the coordinator's call.

## Trail

Read:
- spec t-282 (whole)
- the diff 33b31ee (whole)
- `stage_guard.py` :455-470 and :595-660 (worktree)
- `exit_gate.py` imports (`import stage_guard as SG`, l.37)
- the `hooklib.py` import lines
- `recover_codex_usage.py` imports
- `red_sandbox.py:82`
- `install_paths.py` :598-610
- `planning_contract.py` :3936-3944
- `harness.py` :355-375 and :450-470
- `test-layers.json` row `test_resolver.py` (layer `table`, 35 covers, not in quarantine)
- `plans/builder-rules.md` items 1 and 11
- `docs/tasks/critic-diff-brief.md` items 6-12
- batch-6 file and finding names on `origin/main`
- `tools/critic_verdict.schema.json`

Not opened beyond the given: plan review t-286 (its fixes are reflected in spec §10). `architecture.md` and
`SIBLING_MAP.md` are known through the auto-loaded index and the spec's axis list.

```json
{
  "verdict": "fit",
  "blockers": [],
  "class_completeness": "All 13 sites of spec 2.2 call hooklib.is_one_component in their own direction and position. My own case-insensitive greps over scripts/*.py (the separator literal, the dot tuple/set, the Path(x).name and basename forms, and the slash-in-x-or form, with hooklib.py:272 as the positive control) leave only the spec 2.4 sites: event_store.py:482, selftest.py:982, and dependency_drift.py:92 in the stated blind spot. OH61_ALLOWED equals exactly the two pattern-visible ones. The remainder is queued: on origin/main the finding 20261113-is-one-component-kopii-vne-oh6-1.md names all three, plus the F-3 (NTFS) and F-8 (silent skip) findings. Axis 8 row: queued to Lead (F-6). Axis 18: new shrink-only allowance born at its floor. Axis 34: one road.",
  "trail": {
    "read": [
      "docs/tasks/specs/t-282-oh6-1-one-component.md",
      "git diff 33b31ee~1 33b31ee (13 files)",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/stage_guard.py:455-470,595-660",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/exit_gate.py imports",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/hooklib.py imports",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/install_paths.py:598-610",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/planning_contract.py:3936-3944",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/tests/harness.py:355-375,450-470",
      ".claude/worktrees/oh6-1/ai-packages/qa-factory/scripts/tests/test-layers.json row test_resolver.py",
      "plans/builder-rules.md items 1, 11",
      "docs/tasks/critic-diff-brief.md items 6-12",
      "origin/main plans/piles/onboarding-hooks/findings/20261113-is-one-component-kopii-vne-oh6-1.md",
      "tools/critic_verdict.schema.json"
    ],
    "reruns": [
      {"command": "python -B scripts/tests/test_resolver.py (worktree package dir)", "result": "=== test_resolver: 437/437 ok ===; 215 PASS OH6-1 lines (105 cells + 98 spy + 12 sentinel)"},
      {"command": "python -B scripts/tests/test_judgment_census.py (worktree package dir)", "result": "=== judgment_census: 22/22 ok ===; breach=1 validate_artifacts.py::check_behaviour_claims, a file untouched by the diff (pre-existing)"},
      {"command": "Grep -i over scripts/*.py for the four copy forms", "result": "only the spec 2.4 sites remain; hooklib.py:272 is the positive control"}
    ]
  }
}
```
